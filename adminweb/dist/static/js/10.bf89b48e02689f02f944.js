webpackJsonp([10],{Ap4a:function(e,t,a){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var s={name:"todolist",data:function(){return{tableData:[],cur_page:1,multipleSelection:[],select_cate:"",select_word:"",del_list:[],is_search:!1,editVisible:!1,resetVisible:!1,form:{name:"",role:"",phone:""},idx:-1,cid:"",pagenum:0,totalnum:0}},filters:{formatTime:function(e,t){var a=new Date(e),s=a.getFullYear(),o=a.getMonth()+1,i=a.getDate(),n=a.getHours(),r=a.getMinutes(),c=a.getSeconds(),d="";return void 0==t&&(d=s+"-"+(o<10?"0"+o:o)+"-"+(i<10?"0"+i:i)+" "+(n<10?"0"+n:n)+":"+(r<10?"0"+r:r)+":"+(c<10?"0"+c:c)),"yyyy-mm-dd"==t&&(d=s+"-"+(o<10?"0"+o:o)+"-"+(i<10?"0"+i:i)),"yyyy-mm"==t&&(d=s+"-"+(o<10?"0"+o:o)),"mm-dd"==t&&(d=" "+(mm<10?"0"+mm:mm)+":"+(ddmin<10?"0"+dd:dd)),"hh:mm"==t&&(d=" "+(n<10?"0"+n:n)+":"+(r<10?"0"+r:r)),d}},created:function(){this.getData()},computed:{},methods:{formatType:function(e){return 0==e.type?"新任务":1==e.type?"车辆":2==e.type?"领任务":3==e.type?"提交任务":4==e.type?"收入提现":"未知"},formatIsdone:function(e){return 0==e.isDone?"未处理":1==e.isDone?"已处理":"未知"},handleCurrentChange:function(e){var t=this;this.pagenum=e-1,this.otableData="",setTimeout(function(){t.getData(t.jid)},300)},getData:function(){var e=this;this.$axios.get("/ctb/check/getStayAdminCheck",{params:{openId:"10000",userId:"4",page:this.pagenum,pageSize:15}}).then(function(t){1==t.data.code?(e.totalnum=t.data.totalNum,e.tableData=t.data.data):e.$message.error(t.data.msg)})},search:function(){this.is_search=!0},handleEdit:function(e,t){this.idx=e;var a=this.tableData[e];this.form={name:a.name,phone:a.phone,trueName:a.trueName,address:a.address},this.editVisible=!0},dotypefail:function(e){var t=this;0==e?this.$message.success("测试新任务拒绝审核"):1==e?this.$axios.get("/ctb/check/adminCheckCarInfo",{params:{openId:"10000",userId:"4",checkId:this.cid,isDone:2}}).then(function(e){1==e.code?(t.$message.success("拒绝审核成功"),t.getData()):t.$message.error(e.data.msg)}):2==e?this.$axios.get("/ctb/check/adminCheckGetTask",{params:{openId:"10000",userId:"4",checkId:this.cid,isDone:2}}).then(function(e){1==e.code?(t.$message.error("拒绝审核成功"),t.getData()):t.$message.error(e.data.msg)}):3==e?this.$axios.get("/ctb/check/adminCheckDoTask",{params:{openId:"10000",userId:"4",checkId:this.cid,isDone:2}}).then(function(e){1==e.code?(t.$message.error("拒绝审核成功"),t.getData()):t.$message.error(e.data.msg)}):4==e&&this.$axios.get("/ctb/check/adminCheckOutStream",{params:{openId:"10000",userId:"4",checkId:this.cid,isDone:2}}).then(function(e){1==e.code?(t.$message.error("拒绝审核成功"),t.getData()):t.$message.error(e.data.msg)})},dotypesuccess:function(e){var t=this;0==e?this.$message.success("测试新任务审核"):1==e?this.$axios.get("/ctb/check/adminCheckCarInfo",{params:{openId:"10000",userId:"4",checkId:this.cid,isDone:1}}).then(function(e){1==e.code?(t.$message.success("审核成功"),t.getData()):t.$message.error(e.data.msg)}):2==e?this.$axios.get("/ctb/check/adminCheckGetTask",{params:{openId:"10000",userId:"4",checkId:this.cid,isDone:1}}).then(function(e){1==e.code?(t.$message.error("审核成功"),t.getData()):t.$message.error(e.data.msg)}):3==e?this.$axios.get("/ctb/check/adminCheckDoTask",{params:{openId:"10000",userId:"4",checkId:this.cid,isDone:1}}).then(function(e){1==e.code?(t.$message.error("审核成功"),t.getData()):t.$message.error(e.data.msg)}):4==e&&this.$axios.get("/ctb/check/adminCheckOutStream",{params:{openId:"10000",userId:"4",checkId:this.cid,isDone:1}}).then(function(e){1==e.code?(t.$message.error("审核成功"),t.getData()):t.$message.error(e.data.msg)})},dofail:function(e,t){var a=this;console.log(t.type),this.cid=t.id,this.$confirm("确认审核失败吗?","提示",{confirmButtonText:"确定失败",cancelButtonText:"取消",type:"warning"}).then(function(){a.dotypefail(t.type)}).catch(function(){})},dowell:function(e,t){var a=this;console.log(t.type),this.cid=t.id,this.$confirm("确认审核通过吗?","提示",{confirmButtonText:"确定通过",cancelButtonText:"取消",type:"success"}).then(function(){a.dotypesuccess(t.type)}).catch(function(){})},saveEdit:function(e,t){var a=this,s=this.tableData[this.idx].id,o=this.tableData[this.idx].openId;this.$axios.get("/ctb/user/perfectUserInfo",{params:{openId:o,userId:s,phone:this.form.phone,trueName:this.form.trueName,address:this.form.address}}).then(function(e){console.log(e),1==e.data.code?(a.editVisible=!1,a.$message.success("用户信息修改成功"),a.form.name="",a.form.phone="",a.form.trueName="",a.form.address="",a.getData()):a.$message.error(e.data.msg)})},refresh:function(e,t){this.getData()}}},o={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"table"},[a("div",{staticClass:"crumbs"},[a("el-breadcrumb",{attrs:{separator:"/"}},[a("el-breadcrumb-item",[a("i",{staticClass:"el-icon-lx-cascades"}),e._v(" 待处理审核列表")])],1)],1),e._v(" "),a("div",{staticClass:"container"},[a("div",{staticClass:"handle-box"},[a("el-button",{staticClass:"add",attrs:{type:"primary",icon:"search"},on:{click:e.refresh}},[e._v("刷新")])],1),e._v(" "),a("el-table",{ref:"multipleTable",staticClass:"table",attrs:{data:e.tableData,border:""}},[a("el-table-column",{attrs:{prop:"id",label:"id号",width:"100"}}),e._v(" "),a("el-table-column",{attrs:{prop:"businessId",label:"处理任务号",width:"100"}}),e._v(" "),a("el-table-column",{attrs:{prop:"name",label:"昵称",width:"120"}}),e._v(" "),a("el-table-column",{attrs:{prop:"type",label:"类型",formatter:e.formatType,width:"130"}}),e._v(" "),a("el-table-column",{attrs:{align:"center",label:"提交时间",width:"180"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("p",[e._v("\n            "+e._s(e._f("formatTime")(t.row.createTime))+"\n          ")])]}}])}),e._v(" "),a("el-table-column",{attrs:{prop:"isDone",label:"处理状态",width:"110",formatter:e.formatIsdone}}),e._v(" "),a("el-table-column",{attrs:{label:"操作",width:"230",align:"center"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-button",{attrs:{type:"text",icon:"el-icon-lx-roundclose"},on:{click:function(a){e.dofail(t.$index,t.row)}}},[e._v("审核失败")]),e._v(" "),a("el-button",{attrs:{type:"text",icon:"el-icon-lx-roundcheck"},on:{click:function(a){e.dowell(t.$index,t.row)}}},[e._v("审核通过")])]}}])})],1),e._v(" "),a("div",{staticClass:"pagination"},[a("el-pagination",{attrs:{background:"",layout:"prev, pager, next",total:e.totalnum},on:{"current-change":e.handleCurrentChange}})],1)],1),e._v(" "),a("el-dialog",{attrs:{title:"编辑",visible:e.editVisible,width:"30%"},on:{"update:visible":function(t){e.editVisible=t}}},[a("el-form",{ref:"form",attrs:{model:e.form,"label-width":"70px"}},[a("el-form-item",{attrs:{label:"姓名"}},[a("el-input",{model:{value:e.form.name,callback:function(t){e.$set(e.form,"name",t)},expression:"form.name"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"真实姓名"}},[a("el-input",{model:{value:e.form.trueName,callback:function(t){e.$set(e.form,"trueName",t)},expression:"form.trueName"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"手机号"}},[a("el-input",{model:{value:e.form.phone,callback:function(t){e.$set(e.form,"phone",t)},expression:"form.phone"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"地址"}},[a("el-input",{model:{value:e.form.address,callback:function(t){e.$set(e.form,"address",t)},expression:"form.address"}})],1)],1),e._v(" "),a("span",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{on:{click:function(t){e.editVisible=!1}}},[e._v("取 消")]),e._v(" "),a("el-button",{on:{click:e.saveEdit}},[e._v("确 定")])],1)],1)],1)},staticRenderFns:[]};var i=a("VU/8")(s,o,!1,function(e){a("tKIk")},"data-v-69e4a170",null);t.default=i.exports},tKIk:function(e,t){}});