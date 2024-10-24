class Game {
  constructor(size = 4) {
    this.size = size;
    this.grid = [];
    this.score = 0;
    this.init();
  }

  init() {
    this.grid = Array(this.size).fill().map(() => Array(this.size).fill(0));
    this.addRandomTile();
    this.addRandomTile();
  }

  addRandomTile() {
    const emptyCells = [];
    for (let i = 0; i < this.size; i++) {
      for (let j = 0; j < this.size; j++) {
        if (this.grid[i][j] === 0) {
          emptyCells.push({ x: i, y: j });
        }
      }
    }

    if (emptyCells.length > 0) {
      const { x, y } = emptyCells[Math.floor(Math.random() * emptyCells.length)];
      this.grid[x][y] = Math.random() < 0.9 ? 2 : 4;
    }
  }

  move(direction) {
    let moved = false;

    switch (direction) {
      case 'left':
        moved = this.moveLeft();
        break;
      case 'right':
        moved = this.moveRight();
        break;
      case 'up':
        moved = this.moveUp();
        break;
      case 'down':
        moved = this.moveDown();
        break;
    }

    if (moved) {
      this.addRandomTile();
    }

    return moved;
  }

  moveLeft() {
    return this.moveHorizontal(false);
  }

  moveRight() {
    return this.moveHorizontal(true);
  }

  moveUp() {
    return this.moveVertical(false);
  }

  moveDown() {
    return this.moveVertical(true);
  }

  moveHorizontal(isRight) {
    let moved = false;
    for (let i = 0; i < this.size; i++) {
      const row = isRight ? this.grid[i].slice().reverse() : this.grid[i].slice();
      const newRow = this.mergeLine(row);
      if (isRight) newRow.reverse();
      
      if (!this.arraysEqual(this.grid[i], newRow)) {
        this.grid[i] = newRow;
        moved = true;
      }
    }
    return moved;
  }

  moveVertical(isDown) {
    let moved = false;
    for (let j = 0; j < this.size; j++) {
      const column = [];
      for (let i = 0; i < this.size; i++) {
        column.push(this.grid[i][j]);
      }
      
      const newColumn = isDown ? this.mergeLine(column.reverse()) : this.mergeLine(column);
      if (isDown) newColumn.reverse();

      if (!this.arraysEqual(column, newColumn)) {
        for (let i = 0; i < this.size; i++) {
          this.grid[i][j] = newColumn[i];
        }
        moved = true;
      }
    }
    return moved;
  }

  mergeLine(line) {
    const newLine = line.filter(cell => cell !== 0);
    for (let i = 0; i < newLine.length - 1; i++) {
      if (newLine[i] === newLine[i + 1]) {
        newLine[i] *= 2;
        this.score += newLine[i];
        newLine.splice(i + 1, 1);
      }
    }
    while (newLine.length < this.size) {
      newLine.push(0);
    }
    return newLine;
  }

  arraysEqual(arr1, arr2) {
    return JSON.stringify(arr1) === JSON.stringify(arr2);
  }

  isGameOver() {
    for (let i = 0; i < this.size; i++) {
      for (let j = 0; j < this.size; j++) {
        if (this.grid[i][j] === 0) {
          return false;
        }
        if (
          (i < this.size - 1 && this.grid[i][j] === this.grid[i + 1][j]) ||
          (j < this.size - 1 && this.grid[i][j] === this.grid[i][j + 1])
        ) {
          return false;
        }
      }
    }
    return true;
  }

  updateBestScore() {
    // This method is not implemented in the original code
  }
}

// 创建游戏实例
const game = new Game();

// 在这里添加事件监听器来处理用户输入
wx.onTouchStart(function(e) {
  // 处理触摸开始
});

wx.onTouchEnd(function(e) {
  // 处理触摸结束，移动方块
});

// 导出游戏实例，以便在其他地方使用
export default game;
