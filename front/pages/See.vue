<template>
  <div class="See">
    <div class="header">
      <div>{{data.filename}}</div>
      <div>
        <el-button-group>
          <el-button type="primary" size="mini" @click="doCopy">
            <i class="fa fa-copy"></i>&nbsp;复制
          </el-button>
          <el-button size="mini" @click="doDownload">
            <i class="fa fa-download"></i>&nbsp;下载
          </el-button>
        </el-button-group>
      </div>
    </div>
    <div class="body">
      <pre v-html="renderedCode"></pre>
    </div>
  </div>
</template>
<script>
const axios = require("../js/ajax");
const urlParser = require("url");
const highlight = require("highlight.js");
const qs = require("querystring");
import "highlight.js/styles/tomorrow.css";
export default {
  data() {
    return {
      data: { filename: "", content: "" }
    };
  },
  mounted() {
    const urlStruct = urlParser.parse(location.href);
    const query = qs.parse(urlStruct.query);
    const filename = query.q;
    document.title = filename;
    axios
      .get("/api/get_file", {
        params: {
          filename
        }
      })
      .then(resp => {
        this.data = resp.data;
      });
  },
  computed: {
    renderedCode() {
      const res = highlight.highlightAuto(this.data.content);
      return res.value;
    }
  },
  methods: {
    doDownload() {
      this.download(this.data.content, this.data.filename);
    },
    doCopy() {
      this.copyText(this.data.content);
      this.$message("复制成功");
    },
    download(content, fileName) {
      var aEle = document.createElement("a"),
        blob = new Blob([content]);
      aEle.download = fileName;
      aEle.href = URL.createObjectURL(blob);
      aEle.click();
    },
    copyText(text) {
      var textarea = document.createElement("textarea"); //创建input对象
      var currentFocus = document.activeElement; //当前获得焦点的元素
      var toolBoxwrap = document.querySelector(".body"); //将文本框插入到NewsToolBox这个之后
      toolBoxwrap.appendChild(textarea); //添加元素
      textarea.value = text;
      textarea.focus();
      if (textarea.setSelectionRange) {
        textarea.setSelectionRange(0, textarea.value.length); //获取光标起始位置到结束位置
      } else {
        textarea.select();
      }
      var flag = document.execCommand("copy"); //执行复制
      toolBoxwrap.removeChild(textarea); //删除元素
      currentFocus.focus();
      return flag;
    }
  }
};
</script>
<style lang="less">
@import url("../common.less");
.See {
  .fillParent();
  overflow: auto;

  @header-height: 40px;
  .header {
    display: flex;
    justify-content: space-between;
    height: @header-height;
    background: #eeeeee;
    padding-left: 20px;
    padding-right: 20px;
    align-items: center;
  }
  .body {
    height: calc(~"100% - " @header-height);
    overflow: auto;
    display: flex;
    justify-content: center;
    pre {
      border: 1px;
      border-style: solid;
      border-color: #dddddd;
      width: fit-content;
      max-width: 90%;
      overflow: auto;
      white-space: pre-wrap;
      height: fit-content;
      padding: 25px;
    }
  }
}
</style>

