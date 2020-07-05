//下面是methods中的内容
// 图片转换格式的方法 直接使用就好  不需要知道为什么
function dataURLToBlob(dataurl){
  let arr = dataurl.split(',');
  let mime = arr[0].match(/:(.*?);/)[1];
  let bstr = atob(arr[1]);
  let n = bstr.length;
  let u8arr = new Uint8Array(n);
  while (n--) {
    u8arr[n] = bstr.charCodeAt(n);
  }
  return new Blob([u8arr], {type: mime});
}
/*保存图片的方法（即按钮点击触发的方法）
    第一个参数为需要保存的div的id名
    第二个参数为保存图片的名称 */
function
  saveImage(divText, imgText){
  let canvasID = window.this.$refs[divText];
  let that = window.this;
  let a = document.createElement('a');
  window.html2canvas(canvasID, {scrollY: -scrollY, scrollX: -scrollX}).then(canvas => {
    let dom = document.body.appendChild(canvas);
    // dom.style.display = 'none';
    // a.style.display = 'none';
    document.body.removeChild(dom);
    let blob = dataURLToBlob(dom.toDataURL('image/png'));
    a.setAttribute('href', URL.createObjectURL(blob));
    //这块是保存图片操作  可以设置保存的图片的信息
    a.setAttribute('download', imgText + '.png');
    document.body.appendChild(a);
    a.click();
    URL.revokeObjectURL(blob);
    document.body.removeChild(a);
  });
}

export {
  dataURLToBlob, saveImage
}
