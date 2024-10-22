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
        if (!boardElement) {
            console.error('Game board element not found.');
            return; // 如果找不到游戏板，停止执行
        }

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
            return; // 如果游戏结束或该位置已被占用或不是当前玩家，返回
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
        this.currentPlayer = player === 'black' ? 'white' : 'black'; // 切换当前玩家
        this.updateCurrentPlayerDisplay();
    }

    updateCell(row, col, player) {
        const cell = document.querySelector(`.cell[data-row="${row}"][data-col="${col}"]`);
        if (cell) { // 确保 cell 存在
            const piece = document.createElement('div');
            piece.classList.add('piece', player);
            cell.appendChild(piece);
        } else {
            console.error(`Cell at (${row}, ${col}) not found.`);
        }
    }

    updateCurrentPlayerDisplay() {
        const currentPlayerElement = document.getElementById('current-player');
        if (currentPlayerElement) {
            currentPlayerElement.textContent = this.currentPlayer === 'black' ? '黑子' : '白子';
        } else {
            console.error('Current player display element not found.');
        }
    }

    endGame(winner) {
        this.gameOver = true;
        alert(winner ? `游戏结束，${winner}获胜！` : '游戏结束，平局！');
    }
}

// 使用立即执行函数来避免全局变量污染
(function() {
    function initializeGame() {
        const gameBoard = document.getElementById('game-board');
        if (gameBoard) {
            const gameId = gameBoard.dataset.gameId;
            const playerColor = gameBoard.dataset.playerColor;
            if (gameId && playerColor) {
                new GobangGame(gameId, playerColor);
            } else {
                console.log('Game ID or player color not found.');
            }
        } else {
            console.log('Game board not found. This might not be a game page.');
        }
    }

    // 当 DOM 加载完成时初始化游戏
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeGame);
    } else {
        initializeGame();
    }
})();
