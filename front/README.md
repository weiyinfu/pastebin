* xkeditor:https://www.npmjs.com/package/xkeditor
* mavoneditor:https://www.npmjs.com/package/mavon-editor


chrome bookmark的需求：
* 要有快捷键
* 支持多选
* 支持撤销


集成markdown编辑
按照创建时间
按照修改时间排序

原则：
自己好用就行
把wiki/github整合进来

文章：增删改查

 [
    ["bold", "italic", "underline", "strike"],
    ["blockquote", "code-block"],
    [{ header: 1 }, { header: 2 }],
    [{ list: "ordered" }, { list: "bullet" }],
    [{ script: "sub" }, { script: "super" }],
    [{ indent: "-1" }, { indent: "+1" }],
    [{ direction: "rtl" }],
    [{ size: ["small", false, "large", "huge"] }],
    [{ header: [1, 2, 3, 4, 5, 6, false] }],
    [{ color: [] }, { background: [] }],
    [{ font: [] }],
    [{ align: [] }],
    ["clean"],
    ["link", "image", "video"]
]