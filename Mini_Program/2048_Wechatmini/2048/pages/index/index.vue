<template>
	<view class="container" @touchstart="touchStart" @touchend="touchEnd">
		<view class="game-board" :style="gameBoardStyle">
			<view v-for="(row, i) in game.grid" :key="i" class="row">
				<view v-for="(cell, j) in row" :key="j" 
					  class="cell" 
					  :class="`cell-${cell}`"
					  :style="cellStyle">
					{{ cell !== 0 ? cell : '' }}
				</view>
			</view>
		</view>
		<view class="score-container">
			<view class="score">分数: {{ game.score }}</view>
			<view class="best-score">最高分: {{ game.bestScore }}</view>
		</view>
		<view class="button-container">
			<button @click="resetGame">重新开始</button>
			<button @click="undo">撤销</button>
			<button @click="goToSettings">设置</button>
			<button @click="goToRanking">排行榜</button>
		</view>
	</view>
</template>

<script>
import Game from '../../js/game.js';

export default {
	data() {
		return {
			game: null,
			touchStartX: 0,
			touchStartY: 0,
			gridSize: 4
		};
	},
	computed: {
		gameBoardStyle() {
			return {
				gridTemplateColumns: `repeat(${this.gridSize}, 1fr)`
			};
		},
		cellStyle() {
			const size = 300 / this.gridSize - 10;
			return {
				width: `${size}px`,
				height: `${size}px`,
				fontSize: `${size / 3}px`
			};
		}
	},
	onShow() {
		this.checkLoginStatus();
		const settings = uni.getStorageSync('gameSettings');
		if (settings) {
			this.gridSize = parseInt(settings.gridSizeIndex) + 3;
		}
		this.resetGame();
	},
	methods: {
		resetGame() {
			this.game = new Game(this.gridSize);
			this.game.init();
		},
		touchStart(event) {
			this.touchStartX = event.touches[0].clientX;
			this.touchStartY = event.touches[0].clientY;
		},
		touchEnd(event) {
			const touchEndX = event.changedTouches[0].clientX;
			const touchEndY = event.changedTouches[0].clientY;
			const dx = touchEndX - this.touchStartX;
			const dy = touchEndY - this.touchStartY;

			const absDx = Math.abs(dx);
			const absDy = Math.abs(dy);

			if (Math.max(absDx, absDy) > 10) {
				if (absDx > absDy) {
					this.game.move(dx > 0 ? 'right' : 'left');
				} else {
					this.game.move(dy > 0 ? 'down' : 'up');
				}
			}

			if (this.game.isGameOver()) {
				uni.showModal({
					title: '游戏结束',
					content: `您的得分是: ${this.game.score}`,
					showCancel: false,
					confirmText: '重新开始',
					success: () => {
						this.uploadScore(this.game.score);
						this.resetGame();
					}
				});
			}
		},
		undo() {
			if (this.game.undo()) {
				// 撤销成功
			} else {
				uni.showToast({
					title: '无法撤销',
					icon: 'none'
				});
			}
		},
		goToSettings() {
			uni.navigateTo({
				url: '/pages/settings/settings'
			});
		},
		goToRanking() {
			uni.navigateTo({
				url: '/pages/ranking/ranking'
			});
		},
		checkLoginStatus() {
			const userInfo = uni.getStorageSync('userInfo');
			if (!userInfo) {
				uni.navigateTo({
					url: '/pages/login/login'
				});
			}
		},
		uploadScore(score) {
			const userInfo = uni.getStorageSync('userInfo');
			if (userInfo) {
				const user = JSON.parse(userInfo);
				// 这里应该调用微信云开发的数据库API来上传分数
				console.log(`上传分数：${user.nickName} - ${score}`);
			}
		}
	}
};
</script>

<style>
.container {
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: 20px;
}

.game-board {
	display: grid;
	gap: 10px;
	background-color: #bbada0;
	border-radius: 6px;
	padding: 10px;
	width: 300px;
	height: 300px;
}

.cell {
	display: flex;
	justify-content: center;
	align-items: center;
	font-weight: bold;
	border-radius: 3px;
	transition: all 0.1s ease-in-out;
}

.cell-0 { background-color: #ccc0b3; }
.cell-2 { background-color: #eee4da; }
.cell-4 { background-color: #ede0c8; }
.cell-8 { background-color: #f2b179; color: #f9f6f2; }
.cell-16 { background-color: #f59563; color: #f9f6f2; }
.cell-32 { background-color: #f67c5f; color: #f9f6f2; }
.cell-64 { background-color: #f65e3b; color: #f9f6f2; }
.cell-128 { background-color: #edcf72; color: #f9f6f2; }
.cell-256 { background-color: #edcc61; color: #f9f6f2; }
.cell-512 { background-color: #edc850; color: #f9f6f2; }
.cell-1024 { background-color: #edc53f; color: #f9f6f2; }
.cell-2048 { background-color: #edc22e; color: #f9f6f2; }

.score-container {
	display: flex;
	justify-content: space-between;
	width: 100%;
	margin-top: 20px;
}

.score, .best-score {
	font-size: 18px;
}

.button-container {
	display: flex;
	justify-content: space-between;
	width: 100%;
	margin-top: 20px;
}

.button-container button {
	width: 45%;
}

@keyframes appear {
  0% { opacity: 0; transform: scale(0); }
  100% { opacity: 1; transform: scale(1); }
}

@keyframes pop {
  0% { transform: scale(1); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}

.cell-new {
  animation: appear 0.2s ease-in-out;
}

.cell-merged {
  animation: pop 0.2s ease-in-out;
}
</style>
