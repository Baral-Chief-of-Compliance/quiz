import{h as c,z as f,A as a}from"./index.0112ab5c.js";function v(n,t){return n!==void 0&&n()||t}function d(n,t){if(n!==void 0){const r=n();if(r!=null)return r.slice()}return t}function l(n,t){return n!==void 0?t.concat(n()):t}function h(n,t){return n===void 0?t:t!==void 0?t.concat(n()):n()}function g(n,t,r,e,i,u){t.key=e+i;const o=c(n,t,r);return i===!0?f(o,u()):o}function S(n,t){const r=n.style;for(const e in t)r[e]=t[e]}function y(n){if(n==null)return;if(typeof n=="string")try{return document.querySelector(n)||void 0}catch{return}const t=a(n);if(t)return t.$el||t}function m(n,t){if(n==null||n.contains(t)===!0)return!0;for(let r=n.nextElementSibling;r!==null;r=r.nextElementSibling)if(r.contains(t))return!0;return!1}export{l as a,d as b,S as c,g as d,h as e,m as f,y as g,v as h};
