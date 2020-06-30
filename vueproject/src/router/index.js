import Vue from 'vue'
import Router from 'vue-router'
import 'semantic-ui-css/semantic.min.css'
import HelloWorld from '@/components/HelloWorld'
import User from "@/components/User"
import Name from "@/components/Name";
import Market from "@/components/Market";


Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/user',
      name: 'User',
      component: User
    },
    {
      path: '/name',
      name: 'Name',
      component: Name
    },
    {
      path: '/market',
      name: 'Market',
      component: Market
    },
  ]
})
