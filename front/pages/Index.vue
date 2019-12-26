
<template>
  <div class="Index">
    <div class="wrapper">
      <div>
        <el-input v-model="data.filename" placeholder="请输入标题" autofocus></el-input>
      </div>
      <el-input
        v-model="data.content"
        type="textarea"
        :autosize="{minRows:10}"
        class="code"
        placeholder="请粘贴代码"
      ></el-input>
      <el-button class="submit-button" @click="post" size="large" type="primary">发布</el-button>
    </div>
  </div>
</template>
<script>
const axios = require("axios");
const qs=require("querystring")
export default {
  data() {
    return {
      data: {
        filename: "",
        content: ""
      }
    };
  },
  mounted() {},
  methods: {
    post() {
      axios
        .post("/api/put_file", this.data)
        .then(resp => {
          console.log(resp);
          if ((resp.data = "ok")) {
            location.href="See.html?"+qs.stringify({q:this.data.filename})
            this.$message("发布成功");
          } else {
            this.$message("发布失败");
          }
        })
        .catch(e => {
          this.$message("发布失败");
        });
    }
  }
};
</script>
<style lang="less">
@import url("../common.less");
.Index {
  .fillParent();
  display: flex;
  justify-content: center;
  height: 100%;
  overflow:auto ;
  .wrapper {
    width: 80%;
    > * {
      margin-top: 10px;
    }
    .submit-button {
      width: 100%;
    }
  }
}
</style>