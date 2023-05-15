const NotFoundComponent = { template: '<p>Page not found</p>' }

// 创建一个Vue 应用
const routes = [
    { path: '/:catchAll(.*)', name: 'Home', component: () => import('../views/home/index.vue') },
    { path: '/foo', component: NotFoundComponent },
    { path: '/Job', name: 'Job', component: () => import('../views/job/index.vue') },
    { path: '/Life', name: 'Life', component: () => import('../views/life/index.vue') }
]

export default routes
