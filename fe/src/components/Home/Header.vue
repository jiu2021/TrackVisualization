<template>
  <el-page-header :icon="null" title=" " class="header">
    <template #content>
      <span class="text-large font-1000 mr-3"> TrackVisualization </span>
    </template>
    <template #extra>
      <div class="flex items-center">
        <div class="upload">
          <el-select v-model="option" class="m-2 choose-option" placeholder="Select File Type">
            <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
          <el-input v-show="option == 1" class="truth_arr" v-model.trim="truth" placeholder="所有批次序号(','为间隔)" />
          <el-input v-show="option == 3" class="swing_arr" v-model.trim="swing" placeholder="摆臂批次序号(','为间隔)" />
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
import { onMounted, ref, defineEmits } from 'vue';
import { ElMessage, genFileId, UploadInstance, UploadProps, UploadRawFile } from 'element-plus'
import { reqUploadTruth, reqUploadPos, reqUploadRun, reqUserData } from '@/api';
const emit = defineEmits(['getUserInfo'])
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

const truth = ref('');
const swing = ref('');
const uploadFile = (e: any) => {
  const formData = new FormData();
  if (option.value != null) {
    if (option.value == 1) {
      const truth_arr = truth.value.split(',');
      try {
        if (truth_arr.length <= 0) throw new Error("");
        for (let i of truth_arr) {
          if (typeof (parseInt(i)) != 'number' || parseInt(i) % 1 != 0) {
            throw new Error("");
          }
        }
        formData.append('truth_file', e.file);
        formData.append('sample_arr', JSON.stringify(truth_arr));
        reqUploadTruth(formData).then(function (res) {
          if (res.data.code == 200) {
            option.value = 0;
            emit('getUserInfo');
          }
        });
      } catch (error) {
        ElMessage({
          showClose: true,
          message: '请规范填入批次序号',
          type: 'error',
        });
      }
    } else if (option.value == 2) {
      formData.append('pos_file', e.file);
      reqUploadPos(formData).then(function (res) {
        if (res.data.code == 200) {
          emit('getUserInfo');
        }
      });
    } else if (option.value == 3) {
      // formData.append('run_file', e.file)
      // formData.append('swing_arr', JSON.stringify([30, 31, 32]));
      // reqUploadRun(formData)
      const swing_arr = swing.value.split(',');
      try {
        if (swing_arr.length <= 0) throw new Error("");
        for (let i of swing_arr) {
          if (typeof (parseInt(i)) != 'number' || parseInt(i) % 1 != 0) {
            throw new Error("");
          }
        }
        formData.append('run_file', e.file)
        formData.append('swing_arr', JSON.stringify(swing_arr));
        reqUploadRun(formData).then(function (res) {
          if (res.data.code == 200) {
            option.value = 0;
            emit('getUserInfo');
          }
        });
      } catch (error) {
        ElMessage({
          showClose: true,
          message: '请规范填入批次序号',
          type: 'error',
        });
      }
    }
  } else {
    ElMessage({
      showClose: true,
      message: '请先选择上传的文件类型',
      type: 'error',
    });
  }
}
// 显示user
const username = ref('');
onMounted(() => {
  username.value = localStorage.getItem('username') || '';
});

// 多选框
const option = ref(0)
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