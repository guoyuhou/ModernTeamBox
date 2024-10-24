<template>
  <view class="container">
    <button v-if="!hasUserInfo" @click="getUserProfile">微信登录</button>
    <view v-else class="user-info">
      <image :src="userInfo.avatarUrl" class="avatar"></image>
      <text class="nickname">{{ userInfo.nickName }}</text>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      hasUserInfo: false,
      userInfo: {}
    }
  },
  onLoad() {
    this.checkLoginStatus();
  },
  methods: {
    checkLoginStatus() {
      const userInfo = uni.getStorageSync('userInfo');
      if (userInfo) {
        this.hasUserInfo = true;
        this.userInfo = JSON.parse(userInfo);
      }
    },
    getUserProfile() {
      uni.getUserProfile({
        desc: '用于完善会员资料',
        success: (res) => {
          this.userInfo = res.userInfo;
          this.hasUserInfo = true;
          uni.setStorageSync('userInfo', JSON.stringify(res.userInfo));
          uni.navigateBack();
        },
        fail: (err) => {
          console.error('获取用户信息失败', err);
          uni.showToast({
            title: '登录失败',
            icon: 'none'
          });
        }
      });
    }
  }
}
</script>

<style>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}
.user-info {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.avatar {
  width: 128rpx;
  height: 128rpx;
  border-radius: 50%;
  margin-bottom: 20rpx;
}
.nickname {
  font-size: 32rpx;
}
</style>
