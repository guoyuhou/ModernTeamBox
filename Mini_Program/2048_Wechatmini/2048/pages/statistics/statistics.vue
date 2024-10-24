<template>
  <view class="container">
    <view class="stat-item">
      <text>游戏次数：</text>
      <text>{{ gamesPlayed }}</text>
    </view>
    <view class="stat-item">
      <text>总得分：</text>
      <text>{{ totalScore }}</text>
    </view>
    <view class="stat-item">
      <text>平均得分：</text>
      <text>{{ averageScore }}</text>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      gamesPlayed: 0,
      totalScore: 0,
      averageScore: 0
    }
  },
  onShow() {
    this.loadStatistics();
  },
  methods: {
    loadStatistics() {
      this.gamesPlayed = parseInt(uni.getStorageSync('gamesPlayed') || '0');
      this.totalScore = parseInt(uni.getStorageSync('totalScore') || '0');
      this.averageScore = this.gamesPlayed > 0 ? Math.round(this.totalScore / this.gamesPlayed) : 0;
    }
  }
}
</script>

<style>
.container {
  padding: 20px;
}
.stat-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}
</style>
