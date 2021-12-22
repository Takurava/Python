import { createRouter, createWebHistory } from "vue-router";

import Firstpage from "../pages/Firstpage.vue"
import Secondpage from "../pages/Secondpage.vue"
import Thirdpage from "../pages/Thirdpage.vue"
import Createpage from "../pages/Createpage.vue"

const routes = [
	{
		path: "/", // first
		component: Firstpage
	},
	{
		path: "/second",
		component: Secondpage
	},
	{
		path: "/third",
		component: Thirdpage
	},
	{
		path: "/create",
		component: Createpage
	},
]

export default createRouter({
	history: createWebHistory(),
	routes: routes,
})