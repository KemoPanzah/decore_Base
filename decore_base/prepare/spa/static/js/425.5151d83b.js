"use strict";(globalThis["webpackChunkuniform_front"]=globalThis["webpackChunkuniform_front"]||[]).push([[425],{5425:(e,a,l)=>{l.r(a),l.d(a,{default:()=>Me});l(9665);var t=l(9835),i=l(499),s=l(5360);class o extends s.y{constructor(e){super(e),this.app.shrink=this.stretch}get base_view(){let e=null;return this.view_s.forEach((a=>{a.id==this.app.route.params.view_id&&(e=a)})),e}get base_view_dialog_s(){let e=[];for(const a in this.decore.meta){const l=this.decore.meta[a];if(l.class.includes("Decore_dialog")&&"app"!=l.parent_id){let a=this.getParentView(this.decore.meta[l.parent_id]);this.base_view&&this.base_view.id==a.id&&e.push(l)}}return e}getParentView(e){return e.class.includes("Decore_view")?e:this.getParentView(this.decore.meta[e.parent_id])}hideDialogs(){this.base_view_dialog_s.forEach((e=>{this.ref[e.id]&&this.ref[e.id].show&&this.ref[e.id].hideDialog()}))}showMainDialog(e){this.base_view_dialog_s.forEach((a=>{a.id===e?this.ref[a.id]&&this.ref[a.id].showDialog():this.ref[a.id]&&1==this.ref[a.id].show&&this.ref[a.id].hideDialog()}))}showSubDialog(e){this.base_view_dialog_s.forEach((a=>{a.id===e&&this.ref[a.id]&&this.ref[a.id].showDialog()}))}}var n=l(1610);class u{constructor(e){this.rowsPerPageOptions=[4,8,16,32,64,128,265,512,1024],this.rowsPerPage=e,this.page=1}}var r=l(8339);class d extends s.y{constructor(e){super(e),this.ql={},this.route=(0,r.yj)(),this.data=(0,i.qj)(new n.V(this.app.route,this.decore.source[this.source_id],null,this.active_s,{...this.query,...this.route.query})),this.pagination=(0,i.qj)(new u(this.pag_recs)),this.item_menu_row_id=null,this.item_menu_target=!1,this.item_menu_model=!1}get column_s(){let e=[];return e.push({name:"gotos",label:"",field:"gotos"}),e.push({name:"actions",label:"",filed:"actions"}),this.active_s.forEach((a=>{var l={};l=a.class.includes("ForeignKeyField")?{name:a.column_name,label:a.verbose_name,field:function(e){return e[a.name]?e[a.name]["title"]:null},sortable:!0}:{name:a.column_name,label:a.verbose_name,field:a.column_name,sortable:!0},e.push(l)})),e}get rel_view_s(){let e=[];return this.decore.meta.app.base_s.forEach((a=>{a.view_s.forEach((a=>{this.decore.source[a.source_id].field_s.forEach((l=>{l.class.includes("ForeignKeyField")&&this.data.source.model==l.rel_model&&e.push({id:a.id,icon:a.icon,title:a.title,parent_id:a.parent_id,rel_field_name:l.name})}))}))})),e}onItemClick(e,a,l){if("td"==e.target.localName)for(const t of this.dialog_s)if("click"==t.activator){this.app.router.push({name:"dialog",params:{dialog_id:t.id,item_id:a.id},query:this.app.route.query});break}}onItemMenuClick(e,a){this.item_menu_row_id=a.id,this.item_menu_target=e.target,this.item_menu_model=!0}}var c=l(3852),p=l(6970),m=l(6328);const _={inheritAttrs:!1},v=Object.assign(_,{__name:"uf-view-context-menu",setup(e){const a=(0,t.l1)().use;return(e,l)=>{const s=(0,t.up)("q-icon"),o=(0,t.up)("q-item-section"),n=(0,t.up)("q-item"),u=(0,t.up)("q-list"),r=(0,t.up)("q-menu");return(0,t.wg)(),(0,t.j4)(r,{"auto-close":"",target:(0,i.SU)(a).item_menu_target,modelValue:(0,i.SU)(a).item_menu_model,"onUpdate:modelValue":l[0]||(l[0]=e=>(0,i.SU)(a).item_menu_model=e)},{default:(0,t.w5)((()=>[(0,t.Wm)(u,{style:{"min-width":"100px"}},{default:(0,t.w5)((()=>[((0,t.wg)(!0),(0,t.iD)(t.HY,null,(0,t.Ko)((0,i.SU)(a).dialog_s,(e=>((0,t.wg)(),(0,t.iD)("span",{key:e.id},["context"==e.activator?((0,t.wg)(),(0,t.j4)(n,{key:0,dense:"",clickable:"",onClick:l=>(0,i.SU)(a).app.router.push({name:"dialog",params:{dialog_id:e.id,item_id:(0,i.SU)(a).item_menu_row_id},query:(0,i.SU)(a).app.route.query})},{default:(0,t.w5)((()=>[(0,t.Wm)(o,{avatar:""},{default:(0,t.w5)((()=>[(0,t.Wm)(s,{name:e.icon},null,8,["name"])])),_:2},1024),(0,t.Wm)(o,null,{default:(0,t.w5)((()=>[(0,t.Uk)((0,p.zw)(e.title),1)])),_:2},1024)])),_:2},1032,["onClick"])):(0,t.kq)("",!0)])))),128)),((0,t.wg)(!0),(0,t.iD)(t.HY,null,(0,t.Ko)((0,i.SU)(a).action_s,(e=>((0,t.wg)(),(0,t.iD)("span",{key:e.id},["context"==e.activator?((0,t.wg)(),(0,t.j4)(n,{key:0,dense:"",clickable:"",onClick:l=>(0,i.SU)(a).ref[e.id].trigger()},{default:(0,t.w5)((()=>[(0,t.Wm)(o,{avatar:""},{default:(0,t.w5)((()=>[(0,t.Wm)(s,{name:e.icon},null,8,["name"])])),_:2},1024),(0,t.Wm)(o,null,{default:(0,t.w5)((()=>[(0,t.Uk)((0,p.zw)(e.title),1)])),_:2},1024)])),_:2},1032,["onClick"])):(0,t.kq)("",!0)])))),128))])),_:1})])),_:1},8,["target","modelValue"])}}});var h=l(7858),g=l(3246),w=l(490),f=l(1233),b=l(2857),k=l(9984),y=l.n(k);const q=v,S=q;y()(v,"components",{QMenu:h.Z,QList:g.Z,QItem:w.Z,QItemSection:f.Z,QIcon:b.Z});const U={class:"row full-width items-center"},W={class:"col-auto float-left"},D={class:"col"},j={inheritAttrs:!1},x=Object.assign(j,{__name:"uf-view-header-menu",setup(e){const a=(0,t.l1)().use,l=(0,i.iH)(null),s=(0,i.iH)(null),o=(0,t.Fl)((()=>{let e=[];return a.dialog_s.forEach((a=>{"default"==a.activator&&e.push(a)})),a.action_s.forEach((a=>{"default"==a.activator&&e.push(a)})),e})),n=(0,t.Fl)((()=>{let e=[];return a.ql.totalWidth&&s.value&&l.value&&s.value.forEach(((a,t)=>{a.offsetLeft+a.offsetWidth>l.value.offsetWidth&&e.push(t)})),e}));return(0,t.YP)(n,(()=>{s.value&&s.value.forEach(((e,a)=>{n.value.includes(a)?e.classList.add("overflowed"):e.classList.remove("overflowed")}))})),(e,u)=>{const r=(0,t.up)("q-btn"),d=(0,t.up)("q-item-section"),c=(0,t.up)("q-item"),p=(0,t.up)("q-list"),m=(0,t.up)("q-menu");return(0,t.wg)(),(0,t.iD)("div",U,[(0,t._)("div",W,[n.value.length>0?((0,t.wg)(),(0,t.j4)(r,{key:0,class:"float-right text-black",dense:"",round:"",flat:"",icon:"mdi-dots-vertical"},{default:(0,t.w5)((()=>[(0,t.Wm)(m,null,{default:(0,t.w5)((()=>[(0,t.Wm)(p,null,{default:(0,t.w5)((()=>[((0,t.wg)(!0),(0,t.iD)(t.HY,null,(0,t.Ko)(o.value,((e,l)=>((0,t.wg)(),(0,t.iD)("div",{key:e.id},["Decore_dialog"==e.class&&n.value.includes(l)?((0,t.wg)(),(0,t.j4)(c,{key:0,clickable:""},{default:(0,t.w5)((()=>[(0,t.Wm)(d,null,{default:(0,t.w5)((()=>[(0,t.Wm)(r,{class:"text-black no-wrap",flat:"",icon:e.icon,label:e.title,onClick:l=>(0,i.SU)(a).app.router.push({name:"dialog",params:{dialog_id:e.id,item_id:"null"},query:(0,i.SU)(a).app.route.query})},null,8,["icon","label","onClick"])])),_:2},1024)])),_:2},1024)):(0,t.kq)("",!0),"Decore_action"==e.class&&n.value.includes(l)?((0,t.wg)(),(0,t.j4)(c,{key:1,clickable:""},{default:(0,t.w5)((()=>[(0,t.Wm)(d,null,{default:(0,t.w5)((()=>[(0,t.Wm)(r,{class:"text-black no-wrap",flat:"",icon:e.icon,label:e.title,onClick:l=>(0,i.SU)(a).ref[e.id].trigger()},null,8,["icon","label","onClick"])])),_:2},1024)])),_:2},1024)):(0,t.kq)("",!0)])))),128))])),_:1})])),_:1})])),_:1})):(0,t.kq)("",!0)]),(0,t._)("div",D,[(0,t._)("div",{ref_key:"menu",ref:l,class:"row no-wrap items-center"},[((0,t.wg)(!0),(0,t.iD)(t.HY,null,(0,t.Ko)(o.value,(e=>((0,t.wg)(),(0,t.iD)("div",{class:"col-auto",key:e.id},[(0,t._)("div",{ref_for:!0,ref_key:"component",ref:s,class:"menu-item row no-wrap"},["Decore_dialog"==e.class?((0,t.wg)(),(0,t.j4)(r,{key:0,class:"text-black",flat:"",icon:e.icon,label:e.title,onClick:l=>(0,i.SU)(a).app.router.push({name:"dialog",params:{dialog_id:e.id,item_id:e.activator},query:(0,i.SU)(a).app.route.query})},null,8,["icon","label","onClick"])):(0,t.kq)("",!0),"Decore_action"==e.class?((0,t.wg)(),(0,t.j4)(r,{key:1,class:"text-black",flat:"",icon:e.icon,label:e.title,onClick:l=>(0,i.SU)(a).ref[e.id].trigger(e,null,(0,i.SU)(a).data.select_s)},null,8,["icon","label","onClick"])):(0,t.kq)("",!0)],512)])))),128))],512)])])}}});var Z=l(1639),F=l(8879);const Q=(0,Z.Z)(x,[["__scopeId","data-v-50bcf3c2"]]),V=Q;y()(x,"components",{QBtn:F.Z,QMenu:h.Z,QList:g.Z,QItem:w.Z,QItemSection:f.Z});const C={class:"row full-width items-center"},P={class:"col-auto"},H={class:"col-auto"},E={key:0,class:"col"},I={key:1,class:"col"},K={key:2,class:"col full-width"},M={class:"row full-width items-center"},O={class:"col-auto"},Y={class:"col"},z={class:"col-auto"},A={inheritAttrs:!1},T=Object.assign(A,{__name:"uf-view-filter",setup(e){const a=(0,t.l1)().use,l=(0,r.tv)(),s=(0,r.yj)(),o=(0,i.iH)(null),n=(0,i.iH)(null),u=(0,i.iH)("eq"),d=(0,i.iH)(null);function c(){o.value&&!n.value?(o.value=null,h.value=null,d.value=null):o.value&&n.value&&(n.value=null,h.value=null,d.value=null)}const p=(0,t.Fl)((()=>{let e=!1;return!o.value||"ForeignKeyField"!=o.value.class&&"ManyToManyField"!=o.value.class&&"BackrefAccessor"!=o.value.class||(e=!0),e})),m=(0,t.Fl)((()=>{let e=[];return a.filter_s.forEach((l=>{let t=!1;Object.entries(a.data.query).forEach((([e])=>{e.includes(l.name)&&"ForeignKeyField"!=l.class&&(t=!0)})),t||e.push(l)})),e})),_=(0,t.Fl)((()=>{let e,l=[];if("ForeignKeyField"==o.value.class)e=o.value.rel_model;else{let l=a.data.source.rel_field_s.filter((e=>"ForeignKeyField"==e.class&&e.backref==o.value.name||"ManyToManyField"==e.class&&e.name==o.value.name))[0];e="ForeignKeyField"==l.class?l.model:l.rel_model}let t=a.decore.getSourceByModel(e);return t.field_s.forEach((e=>{let t=!1;Object.entries(a.data.query).forEach((([a])=>{a.includes(e.name)&&(t=!0)})),t||"ForeignKeyField"!=e.class&&o.value.filter_fields.includes(e.name)&&l.push(e)})),l})),v=(0,t.Fl)((()=>{let e=[{name:"eq",verbose_name:"==",types:"*"}],a=[];return o.value&&e.forEach((e=>{"*"==e.types&&a.push(e),e.types.includes(o.value.class)&&a.push(e)})),a})),h=(0,i.iH)({});function g(){let e=s.query;o.value&&!p.value?a.data.source.getFilterValues(e,o.value.name,null).then((e=>{h.value=h.value=e.data})):n.value&&p.value&&a.data.source.getFilterValues(e,o.value.name,n.value.name).then((e=>{h.value=e.data}))}function w(){let e={...s.query},a="";p.value?p.value&&(a=a+o.value.name+"__"+n.value.name):a=o.value.name,a=a+"__"+u.value,e[a]=d.value,l.push({path:s.path,query:e})}return(e,l)=>{const r=(0,t.up)("q-btn"),f=(0,t.up)("q-select");return(0,t.wg)(),(0,t.iD)("div",C,[(0,t._)("div",P,[(0,t.Wm)(r,{class:"float-right text-black",dense:"",round:"",flat:"",icon:"mdi-content-save",onClick:l[0]||(l[0]=e=>(0,i.SU)(a).decore.queries.saveQuery((0,i.SU)(s)))})]),(0,t._)("div",H,[(0,t.Wm)(r,{class:"float-right text-black",dense:"",round:"",flat:"",icon:"mdi-undo",onClick:l[1]||(l[1]=e=>c()),disable:!o.value},null,8,["disable"])]),o.value?(0,t.kq)("",!0):((0,t.wg)(),(0,t.iD)("div",E,[(0,t.Wm)(f,{dense:"",outlined:"",modelValue:o.value,"onUpdate:modelValue":[l[2]||(l[2]=e=>o.value=e),l[3]||(l[3]=e=>g())],options:m.value,"option-value":"name","option-label":"verbose_name","options-dense":"",label:"Select field for filtering",style:{width:"100%"}},null,8,["modelValue","options"])])),p.value&&o.value&&!n.value?((0,t.wg)(),(0,t.iD)("div",I,[(0,t.Wm)(f,{dense:"",outlined:"",modelValue:n.value,"onUpdate:modelValue":[l[4]||(l[4]=e=>n.value=e),l[5]||(l[5]=e=>g())],options:_.value,"option-value":"name","option-label":"verbose_name","options-dense":"",label:"Select related field for filtering",style:{width:"100%"}},null,8,["modelValue","options"])])):(0,t.kq)("",!0),p.value&&o.value&&n.value||!p.value&&o.value?((0,t.wg)(),(0,t.iD)("div",K,[(0,t._)("div",M,[(0,t._)("div",O,[(0,t.Wm)(f,{dense:"",outlined:"",modelValue:u.value,"onUpdate:modelValue":l[6]||(l[6]=e=>u.value=e),options:v.value,"option-value":"name","option-label":"verbose_name","options-dense":"","map-options":"","emit-value":""},null,8,["modelValue","options"])]),(0,t._)("div",Y,["eq"==u.value?((0,t.wg)(),(0,t.j4)(f,{key:0,dense:"",outlined:"",modelValue:d.value,"onUpdate:modelValue":l[7]||(l[7]=e=>d.value=e),multiple:"","option-label":"label","option-value":"value","map-options":"","emit-value":"",options:Object.entries(h.value).map((([e,a])=>({label:e,value:a}))),"options-dense":"",label:"Select value for filtering",style:{width:"100%"},disable:!h.value,loading:!h.value},null,8,["modelValue","options","disable","loading"])):(0,t.kq)("",!0)])])])):(0,t.kq)("",!0),(0,t._)("div",z,[(0,t.Wm)(r,{class:"float-right text-black",dense:"",round:"",flat:"",icon:"mdi-database-search",onClick:l[8]||(l[8]=e=>w()),disable:!d.value},null,8,["disable"])])])}}});var B=l(2762);const L=T,$=L;y()(T,"components",{QBtn:F.Z,QSelect:B.Z});const N={class:"row full-width row items-center"},R={class:"col-4"},G={class:"col-4"},J={class:"col-4"},X={class:"row items-center"},ee={class:"col-2"},ae={class:"col"},le={class:"row full-width items-center"},te={inheritAttrs:!1},ie=Object.assign(te,{__name:"uf-view-header",setup(e){const a=(0,t.l1)().use,l=(0,r.yj)();return(e,s)=>{const o=(0,t.up)("q-btn"),n=(0,t.up)("q-input"),u=(0,t.up)("q-toolbar"),r=(0,t.up)("q-chip");return(0,t.wg)(),(0,t.iD)(t.HY,null,[(0,t.Wm)(u,{class:"bg-grey-2"},{default:(0,t.w5)((()=>[(0,t._)("div",N,[(0,t._)("div",R,[(0,t.Wm)(V,{use:(0,i.SU)(a)},null,8,["use"])]),(0,t._)("div",G,[(0,i.SU)(a).filter_s.length>0?((0,t.wg)(),(0,t.j4)($,{key:0,use:(0,i.SU)(a)},null,8,["use"])):(0,t.kq)("",!0)]),(0,t._)("div",J,[(0,t._)("div",X,[(0,t._)("div",ee,[(0,t.Wm)(o,{class:"float-right text-black",dense:"",round:"",flat:"",icon:"clear",disable:!(0,i.SU)(a).data.search,onClick:s[0]||(s[0]=e=>(0,i.SU)(a).data.search=null)},null,8,["disable"])]),(0,t._)("div",ae,[(0,t.Wm)(n,{class:"text-black",dense:"",outlined:"",modelValue:(0,i.SU)(a).data.search,"onUpdate:modelValue":s[1]||(s[1]=e=>(0,i.SU)(a).data.search=e),label:"Fast search in "+(0,i.SU)(a).title},null,8,["modelValue","label"])])])])])])),_:1}),(0,t._)("div",le,[((0,t.wg)(!0),(0,t.iD)(t.HY,null,(0,t.Ko)((0,i.SU)(l).query,((e,a)=>((0,t.wg)(),(0,t.j4)(r,{label:a+"="+e,key:a},null,8,["label"])))),128))])],64)}}});var se=l(1663),oe=l(6611),ne=l(7691);const ue=ie,re=ue;y()(ie,"components",{QToolbar:se.Z,QBtn:F.Z,QInput:oe.Z,QChip:ne.Z});const de={class:"row items-center"},ce={class:"view-footer-pagination col-auto"},pe={class:"col-auto"},me={inheritAttrs:!1},_e=Object.assign(me,{__name:"uf-view-footer",setup(e){const a=(0,t.l1)().use,l=(0,t.Fl)((()=>{let e=Math.ceil(a.data.count/a.pagination.rowsPerPage);return e}));return(e,s)=>{const o=(0,t.up)("q-space"),n=(0,t.up)("q-pagination"),u=(0,t.up)("q-select"),r=(0,t.up)("q-toolbar");return(0,t.wg)(),(0,t.j4)(r,{class:"bg-grey-2"},{default:(0,t.w5)((()=>[(0,t.Wm)(o),(0,t._)("div",de,[(0,t._)("div",ce,[(0,t.Wm)(n,{modelValue:(0,i.SU)(a).pagination.page,"onUpdate:modelValue":s[0]||(s[0]=e=>(0,i.SU)(a).pagination.page=e),max:l.value,"max-pages":5,"direction-links":"","boundary-links":"","boundary-numbers":"",color:"black"},null,8,["modelValue","max"])]),(0,t._)("div",pe,[(0,t.Wm)(u,{modelValue:(0,i.SU)(a).pagination.rowsPerPage,"onUpdate:modelValue":s[1]||(s[1]=e=>(0,i.SU)(a).pagination.rowsPerPage=e),options:(0,i.SU)(a).pagination.rowsPerPageOptions,dense:"",outlined:""},null,8,["modelValue","options"])])])])),_:1})}}});var ve=l(136),he=l(996);const ge=_e,we=ge;y()(_e,"components",{QToolbar:se.Z,QSpace:ve.Z,QPagination:he.Z,QSelect:B.Z});const fe={inheritAttrs:!1},be=Object.assign(fe,{__name:"uf-view-layout",setup(e){const a=(0,t.l1)().use,l=(0,t.Fl)((()=>{let e=0;return a.app.ql.hasOwnProperty("header")&&(e=a.app.ql.header.size),a.app.ql.hasOwnProperty("footer")&&(e+=a.app.ql.footer.size),e})),s=(0,t.Fl)((()=>{let e="0 px";return a.ql.hasOwnProperty("header")&&(e=a.ql.header.size+"px"),e}));return(e,o)=>{const n=(0,t.up)("q-header"),u=(0,t.up)("q-footer"),r=(0,t.up)("q-layout");return(0,t.wg)(),(0,t.iD)(t.HY,null,[(0,t.Wm)(S,{use:(0,i.SU)(a)},null,8,["use"]),(0,t.Wm)(r,{container:"",style:(0,p.j5)({height:`calc(100vh - ${l.value}px)`})},{default:(0,t.w5)((()=>[(0,t.Wm)(m.Z,{use:(0,i.SU)(a)},null,8,["use"]),(0,t.Wm)(n,{class:"bg-white",style:{position:"fixed",width:"100%",top:"0"}},{default:(0,t.w5)((()=>[(0,t.Wm)(re,{use:(0,i.SU)(a)},null,8,["use"])])),_:1}),(0,t._)("div",{class:"view-content",style:(0,p.j5)({"padding-top":s.value})},[(0,t.WI)(e.$slots,"view-content")],4),(0,t.Wm)(u,{class:"bg-white",style:{position:"fixed",width:"100%",bottom:"0"}},{default:(0,t.w5)((()=>[(0,t.Wm)(we,{use:(0,i.SU)(a)},null,8,["use"])])),_:1})])),_:3},8,["style"])],64)}}});var ke=l(7605),ye=l(6602),qe=l(1378);const Se=be,Ue=Se;y()(be,"components",{QLayout:ke.Z,QHeader:ye.Z,QFooter:qe.Z});const We={inheritAttrs:!1},De=Object.assign(We,{__name:"uf-view-table",setup(e){const a=(0,t.l1)().use;a.data.items_mode=!0;const l=(0,t.Fl)((()=>{let e=16,l="0 px";return e+=a.app.ql.header.size,e+=a.app.ql.footer.size,e+=a.ql.header.size,e+=a.ql.footer.size,l="calc(100vh - "+e+"px)",l}));return(e,s)=>{const o=(0,t.up)("q-item-section"),n=(0,t.up)("q-item"),u=(0,t.up)("q-list"),r=(0,t.up)("q-menu"),d=(0,t.up)("q-btn"),c=(0,t.up)("q-td"),m=(0,t.up)("q-table");return(0,t.wg)(),(0,t.j4)(m,{columns:(0,i.SU)(a).column_s,filter:(0,i.SU)(a).data.search,rows:(0,i.SU)(a).data.item_s,style:(0,p.j5)({height:l.value}),class:"sticky-header-table",dense:"",flat:"","hide-bottom":"","row-key":"id",selection:"multiple",pagination:(0,i.SU)(a).pagination,"onUpdate:pagination":s[0]||(s[0]=e=>(0,i.SU)(a).pagination=e),selected:(0,i.SU)(a).data.select_s,"onUpdate:selected":s[1]||(s[1]=e=>(0,i.SU)(a).data.select_s=e),onRowClick:s[2]||(s[2]=(e,l,t)=>{(0,i.SU)(a).onItemClick(e,l,t)})},{"body-cell-gotos":(0,t.w5)((e=>[(0,t.Wm)(c,{props:e},{default:(0,t.w5)((()=>[(0,t.Wm)(d,{dense:"",round:"",flat:"",icon:"mdi-link"},{default:(0,t.w5)((()=>[(0,t.Wm)(r,{"auto-close":""},{default:(0,t.w5)((()=>[(0,t.Wm)(u,{style:{"min-width":"100px"}},{default:(0,t.w5)((()=>[((0,t.wg)(!0),(0,t.iD)(t.HY,null,(0,t.Ko)((0,i.SU)(a).rel_view_s,(a=>((0,t.wg)(),(0,t.j4)(n,{dense:"",key:a.id,to:"/"+a.parent_id+"/"+a.id+"?"+a.rel_field_name+"__eq="+e.row.id},{default:(0,t.w5)((()=>[(0,t.Wm)(o,null,{default:(0,t.w5)((()=>[(0,t.Uk)((0,p.zw)("view "+a.title+" from "+e.row.title),1)])),_:2},1024)])),_:2},1032,["to"])))),128))])),_:2},1024)])),_:2},1024)])),_:2},1024)])),_:2},1032,["props"])])),"body-cell-actions":(0,t.w5)((e=>[(0,t.Wm)(c,{props:e},{default:(0,t.w5)((()=>[(0,t.Wm)(d,{dense:"",round:"",flat:"",icon:"mdi-dots-vertical",onClick:l=>{(0,i.SU)(a).onItemMenuClick(l,e.row)}},null,8,["onClick"])])),_:2},1032,["props"])])),_:1},8,["columns","filter","rows","style","pagination","selected"])}}});var je=l(7580),xe=l(7220);const Ze=De,Fe=Ze;y()(De,"components",{QTable:je.Z,QTd:xe.Z,QBtn:F.Z,QMenu:h.Z,QList:g.Z,QItem:w.Z,QItemSection:f.Z});const Qe={__name:"uf-view",props:{id:{}},setup(e){const a=e,l=(0,i.qj)(new d(a.id));for(const t of l.action_s)new c.B(t.id);return(0,t.bv)((()=>{l.data.setItems();for(const e of l.dialog_s)if("empty"==e.activator||"first"==e.activator||"last"==e.activator){l.app.router.push({name:"dialog",params:{dialog_id:e.id,item_id:e.activator},query:l.app.route.query});break}})),(e,a)=>((0,t.wg)(),(0,t.j4)(Ue,{use:l},{"view-content":(0,t.w5)((()=>["table"==l.type?((0,t.wg)(),(0,t.j4)(Fe,{key:0,use:l},null,8,["use"])):(0,t.kq)("",!0)])),_:1},8,["use"]))}},Ve=Qe,Ce=Ve;var Pe=l(9698);const He={key:0},Ee={__name:"uf-base",props:{base_id:{},view_id:{},dialog_id:{},item_id:{},subdialog_id:{},subitem_id:{}},setup(e){const a=e,l=(0,i.qj)(new o(a.base_id));return(0,t.wF)((()=>{let e=localStorage.getItem("user_token");"dbi_login_dialog"==l.app.route.params.dialog_id||l.app.allow_guest||null!=e||l.app.router.push({name:"login"})})),(0,t.bv)((()=>{"view"===l.app.route.name&&(l.app.expanded_nodes=[],l.app.expanded_nodes.push(l.app.route.params.base_id),l.app.expanded_nodes.push(l.app.route.params.view_id),l.hideDialogs()),"dialog"===l.app.route.name&&(l.app.expanded_nodes=[],l.app.expanded_nodes.push(l.app.route.params.base_id),l.app.expanded_nodes.push(l.app.route.params.view_id),l.showMainDialog(l.app.route.params.dialog_id)),"subdialog"===l.app.route.name&&(l.app.expanded_nodes=[],l.app.expanded_nodes.push(l.app.route.params.base_id),l.app.expanded_nodes.push(l.app.route.params.view_id),l.showMainDialog(l.app.route.params.dialog_id),l.showSubDialog(l.app.route.params.subdialog_id)),(0,t.YP)(l.app.route,(e=>{l.app.expanded_nodes.push(e.params.base_id),"view"===e.name&&l.hideDialogs(),"dialog"===e.name&&l.showMainDialog(e.params.dialog_id),"subdialog"===e.name&&l.showSubDialog(e.params.subdialog_id)}))})),(e,a)=>{const i=(0,t.up)("q-page");return(0,t.wg)(),(0,t.iD)(t.HY,null,[((0,t.wg)(!0),(0,t.iD)(t.HY,null,(0,t.Ko)(l.base_view_dialog_s,(e=>((0,t.wg)(),(0,t.j4)(Pe.Z,{key:e.id,id:e.id},null,8,["id"])))),128)),(0,t.Wm)(i,null,{default:(0,t.w5)((()=>[l.base_view?((0,t.wg)(),(0,t.iD)("span",He,[(0,t.Wm)(Ce,{id:l.base_view.id},null,8,["id"])])):(0,t.kq)("",!0)])),_:1})],64)}}};var Ie=l(9885);const Ke=Ee,Me=Ke;y()(Ee,"components",{QPage:Ie.Z})}}]);