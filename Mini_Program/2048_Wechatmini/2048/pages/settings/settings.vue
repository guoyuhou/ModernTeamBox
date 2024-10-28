<template>
  <view class="container">
    <view class="setting-item">
      <text>网格大小：</text>
      <picker @change="onGridSizeChange" :value="gridSizeIndex" :range="gridSizes">
        <view class="picker">
          {{ gridSizes[gridSizeIndex] }}
        </view>
      </picker>
    </view>
    <view class="setting-item">
      <text>音效：</text>
      <switch :checked="soundEnabled" @change="onSoundChange" />
    </view>
    <button @click="saveSettings">保存设置</button>
  </view>
</template>

<script>
export default {
  data() {
    return {
      gridSizes: ['3x3', '4x4', '5x5'],
      gridSizeIndex: 1,
      soundEnabled: true
    }
  },
  onLoad() {
    // 加载保存的设置
    const settings = uni.getStorageSync('gameSettings');
    if (settings) {
      this.gridSizeIndex = settings.gridSizeIndex;
      this.soundEnabled = settings.soundEnabled;
    }
  },
  methods: {
    onGridSizeChange(e) {
      this.gridSizeIndex = e.detail.value;
    },
    onSoundChange(e) {
      this.soundEnabled = e.detail.value;
    },
    saveSettings() {
      const settings = {
        gridSizeIndex: this.gridSizeIndex,
        soundEnabled: this.soundEnabled
      };
      uni.setStorageSync('gameSettings', settings);
      uni.showToast({
        title: '设置保存成功'
      });
    }
  }
};
</script>

<style>
.container {
  padding: 20px;
}

.setting-item {
  margin-bottom: 20px;
}

.picker {
  width: 100px;
  height: 40px;
  line-height: 40px;
  text-align: center;
  border: 1px solid #ccc;
  border-radius: 5px;
}

</style>
