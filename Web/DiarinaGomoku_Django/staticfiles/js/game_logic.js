class GobangGame {
    constructor(gameId, playerColor) {
        this.gameId = gameId;
        this.playerColor = playerColor;
        this.board = Array(15).fill().map(() => Array(15).fill(null));
        this.currentPlayer = 'black';
        this.gameOver = false;
        this.initializeBoard();
        this.connectWebSocket();
    }

    initializeBoard() {
        const boardElement = document.getElementById('game-board');
        boardElement.innerHTML = '';
        for (let i = 0; i < 15; i++) {
            for (let j = 0; j < 15; j++) {
                const cell = document.createElement('div');
                cell.classList.add('cell');
                cell.dataset.row = i;
                cell.dataset.col = j;
                cell.addEventListener('click', () => this.makeMove(i, j));
                boardElement.appendChild(cell);
            }
        }
    }

    connectWebSocket() {
        this.socket = new WebSocket(`ws://${window.location.host}/ws/game/${this.gameId}/`);
        this.socket.onopen = () => {
            console.log('WebSocket连接成功');
        };
        this.socket.onerror = (error) => {
            console.error('WebSocket连接失败:', error);
        };
        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.action === 'move') {
                this.handleMove(data.row, data.col, data.player);
                if (data.is_finished) {
                    this.endGame(data.winner);
                }
            }
        };
    }

    makeMove(row, col) {
        if (this.gameOver || this.board[row][col] !== null || this.currentPlayer !== this.playerColor) {
            return;
        }
        this.socket.send(JSON.stringify({
            action: 'move',
            row: row,
            col: col
        }));
    }

    handleMove(row, col, player) {
        this.board[row][col] = player;
        this.updateCell(row, col, player);
        this.currentPlayer = player === 'black' ? 'white' : 'black';
        this.updateCurrentPlayerDisplay();
    }

    updateCell(row, col, player) {
        const cell = document.querySelector(`.cell[data-row="${row}"][data-col="${col}"]`);
        const piece = document.createElement('div');
        piece.classList.add('piece', player);
        cell.appendChild(piece);
    }

    updateCurrentPlayerDisplay() {
        const currentPlayerElement = document.getElementById('current-player');
        currentPlayerElement.textContent = this.currentPlayer === 'black' ? '黑子' : '白子';
    }

    endGame(winner) {
        this.gameOver = true;
        alert(winner ? `游戏结束，${winner}获胜！` : '游戏结束，平局！');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const gameId = document.getElementById('game-id').value;
    const playerColor = document.getElementById('player-color').value;
    new GobangGame(gameId, playerColor);
});
