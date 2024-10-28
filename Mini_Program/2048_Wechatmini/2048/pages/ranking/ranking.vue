<template>
  <view class="container">
    <view class="ranking-list">
      <view v-for="(item, index) in rankingList" :key="index" class="ranking-item">
        <text class="rank">{{ index + 1 }}</text>
        <image :src="item.avatarUrl" class="avatar"></image>
        <text class="nickname">{{ item.nickName }}</text>
        <text class="score">{{ item.score }}</text>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      rankingList: []
    }
  },
  onShow() {
    this.getRankingList();
  },
  methods: {
    getRankingList() {
      // 这里应该调用微信云开发的数据库API来获取排行榜数据
      // 以下是模拟数据
      this.rankingList = [
        { avatarUrl: 'https://example.com/avatar1.png', nickName: '玩家1', score: 10000 },
        { avatarUrl: 'https://example.com/avatar2.png', nickName: '玩家2', score: 9000 },
        { avatarUrl: 'https://example.com/avatar3.png', nickName: '玩家3', score: 8000 },
      ];
    }
  }
}
</script>

<style>
.container {
  padding: 20rpx;
}
.ranking-item {
  display: flex;
  align-items: center;
  margin-bottom: 20rpx;
}
.rank {
  width: 60rpx;
  text-align: center;
}
.avatar {
  width: 80rpx;
  height: 80rpx;
  border-radius: 50%;
  margin: 0 20rpx;
}
.nickname {
  flex: 1;
}
.score {
  font-weight: bold;
}
</style>
