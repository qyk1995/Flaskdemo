"use strict";(self["webpackChunkwallet"]=self["webpackChunkwallet"]||[]).push([[123],{3123:function(t,e,s){s.r(e),s.d(e,{default:function(){return c}});var l=function(){var t=this,e=t._self._c;return e("div",[e("div",{staticClass:"queryButton"},[e("el-input",{staticStyle:{width:"300px","margin-right":"10px"},attrs:{placeholder:"请输入钱包地址"},model:{value:t.input.wallet,callback:function(e){t.$set(t.input,"wallet",e)},expression:"input.wallet"}}),e("el-button",{attrs:{type:"primary"},on:{click:t.queryHospot}},[t._v("查询钱包热点")])],1),e("div",{staticClass:"mybutton"},[e("el-tooltip",{staticClass:"item",attrs:{effect:"light",content:"转移热点前请先查询热点",placement:"right-end"}},[e("el-button",{attrs:{type:"primary",plain:""},on:{click:t.transferHospot}},[t._v("热点转移")])],1)],1),e("el-table",{ref:"multipleTable",staticStyle:{width:"100%"},attrs:{data:t.tableData,stripe:"","tooltip-effect":"dark"},on:{"selection-change":t.handleSelectionChange}},[e("el-table-column",{attrs:{type:"selection",align:"center",width:"55"}}),e("el-table-column",{attrs:{type:"index",label:"序号",align:"center",width:"50"}}),e("el-table-column",{attrs:{prop:"hotspont",align:"center",label:"热点地址","show-overflow-tooltip":""}})],1),e("el-dialog",{attrs:{title:"转移热点",visible:t.dialogVisible,width:"50%","before-close":t.handleClose},on:{"update:visible":function(e){t.dialogVisible=e}}},[e("el-form",{ref:"form",attrs:{model:t.form,"label-width":"180px"}},[e("el-form-item",{attrs:{label:"密码",rules:[{required:!0,message:"请输入钱包密码",trigger:"blur"}]}},[e("el-input",{attrs:{type:"password",autocomplete:"off"},model:{value:t.form.password,callback:function(e){t.$set(t.form,"password",e)},expression:"form.password"}})],1),e("el-form-item",{attrs:{label:"热点所属的钱包地址",rules:[{required:!0,message:"请输入钱包地址",trigger:"blur"}]}},[e("el-input",{model:{value:t.form.wallets,callback:function(e){t.$set(t.form,"wallets",e)},expression:"form.wallets"}})],1),e("el-form-item",{attrs:{label:"热点所属的钱包key路径",rules:[{required:!0,message:"请输入钱包key文件路径",trigger:"blur"}]}},[e("el-input",{model:{value:t.form.srckey_paths,callback:function(e){t.$set(t.form,"srckey_paths",e)},expression:"form.srckey_paths"}})],1),e("el-form-item",{staticClass:"itemdemo",attrs:{label:"自定义目的钱包的地址文件"}},[e("el-upload",{ref:"my-upload1",staticClass:"upload-demo",attrs:{action:"",limit:1,"on-exceed":t.handleExceed,"auto-upload":!1,"on-change":t.onchange1}},[e("el-button",{attrs:{slot:"trigger",size:"small",type:"primary"},slot:"trigger"},[t._v("选取文件")]),e("div",{staticClass:"el-upload__tip",attrs:{slot:"tip"},slot:"tip"},[t._v("只能上传txt文件")])],1)],1)],1),e("span",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[e("el-button",{on:{click:function(e){t.dialogVisible=!1}}},[t._v("取 消")]),e("el-button",{attrs:{type:"primary"},on:{click:t.onSubmit}},[t._v("确 定")])],1)],1)],1)},a=[],o=s(5101),i={data(){return{tableData:[],dialogVisible:!1,form:{password:"",wallets:"",srckey_paths:"",hotspots:[]},input:{},file:null}},mounted(){},methods:{handleExceed(t,e){this.$message.warning(`当前限制选择1个文件,本次选择了 ${t.length} 个文件，共选择了 ${t.length+e.length} 个文件`)},handleClose(t){this.$confirm("确认关闭？").then((e=>{t()})).catch((t=>{}))},onSubmit(){this.dialogVisible=!1;let t=new FormData;console.log(this.file),t.append("file",this.file),t.append("password",this.form.password),t.append("hotspots",this.form.hotspots),t.append("wallets",this.form.wallets),t.append("srckey_paths",this.form.srckey_paths),this.updateHotspot(t)},handleSelectionChange(t){this.form.hotspots=[],t.forEach((t=>{this.form.hotspots.push(t.hotspont)}))},onchange1(t){this.file=t.raw},async hotspontList(t){let e=await(0,o.ZI)(t),s=e.data.hotspots;s.forEach((t=>{this.tableData.push({hotspont:t})}))},async updateHotspot(t){let e=await(0,o.dF)(t);1==e.status?this.$message({message:e.msg,type:"success"}):this.$message.error(e.msg)},queryHospot(){this.hotspontList(this.input)},transferHospot(){void 0==this.form.hotspots||this.form.hotspots.length<=0?this.$message.error("未选择热点"):this.dialogVisible=!0}}},r=i,n=s(3736),p=(0,n.Z)(r,l,a,!1,null,"26a0725a",null),c=p.exports}}]);
//# sourceMappingURL=123.1af480c9.js.map