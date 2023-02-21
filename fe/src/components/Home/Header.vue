<template>
  <el-page-header :icon="null" title=" " class="header">
    <template #content>
      <span class="text-large font-1000 mr-3"> TrackVisualization </span>
    </template>
    <template #extra>
      <div class="flex items-center">
        <div class="upload">
          <el-select v-model="value" class="m-2 choose-option" placeholder="Select File Type">
            <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
          <el-upload ref="upload" class="upload-demo" action="" :limit="1" :on-exceed="handleExceed"
            :http-request="uploadFile" :auto-upload="false">
            <template #trigger>
              <el-button type="primary">选择文件</el-button>
            </template>
            <el-button class="ml-3" type="success" @click="submitUpload">
              确认
            </el-button>
          </el-upload>
        </div>
        <el-avatar :size="32" class="mr-3" src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png" />
        <div class="name">{{ username }}</div>
      </div>
    </template>
  </el-page-header>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue';
import { genFileId, UploadInstance, UploadProps, UploadRawFile } from 'element-plus'
import { reqUploadTruth } from '@/api';
const upload = ref<UploadInstance>()

const handleExceed: UploadProps['onExceed'] = (files) => {
  upload.value!.clearFiles()
  const file = files[0] as UploadRawFile
  file.uid = genFileId()
  upload.value!.handleStart(file)
}

const submitUpload = () => {
  upload.value!.submit()
}
const uploadFile = (e: any) => {
  const formData = new FormData()
  formData.append('truth_file', e.file)
  formData.append('sample_arr', JSON.stringify([27, 28, 29, 30, 31, 32]));
  reqUploadTruth(formData)
}
// 显示user
const username = ref('');
onMounted(() => {
  username.value = localStorage.getItem('username') || '';
});

// 多选框
const value = ref(null)
const options = [
  {
    value: 1,
    label: 'groundtruth',
  },
  {
    value: 2,
    label: 'position',
  },
  {
    value: 3,
    label: 'running',
  }
]
</script>

<style scoped>
.text-large {
  font-size: 28px;
}

.flex {
  display: flex;
  justify-content: center;
  align-items: center;
}

.name {
  margin-left: 10px;
}

.upload {
  display: flex;
  align-items: center;
}

.upload-demo {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 10px;
}

.ml-3 {
  margin: 0 10px;
}

.choose-option {
  width: 120px;
}
</style>