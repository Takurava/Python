<script setup>
// import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
	<!-- <img alt="Vue logo" src="./assets/logo.png" />
	<HelloWorld msg="Hello Vue 3 + Vite" />-->

	<nav class="nav">
		<router-link to="/">Первая</router-link>
		<router-link to="/second">Вторая</router-link>
		<router-link to="/third">Третья</router-link>
		<router-link to="/create">Создать</router-link>
	</nav>

	<main class="main">
		<router-view></router-view>
	</main>
</template>

<style>
:root {
	--offset: 32px;
	--offset-half: calc(var(--offset) / 2);
	--width: 1400px;
}
* {
	margin: 0;
	padding: 0;
	box-sizing: border-box;
}

body {
	min-height: 100vh;
}

#app {
	font-family: Avenir, Helvetica, Arial, sans-serif;
	-webkit-font-smoothing: antialiased;
	-moz-osx-font-smoothing: grayscale;
	color: #2c3e50;
	min-height: 100vh;

	max-width: var(--width);
	margin: 0 auto;

	display: grid;
	grid-template-rows: min-content 1fr;
	gap: var(--offset);
}

.nav {
	max-width: max-content;
	margin: 0 auto;
	display: flex;
}

.nav a {
	margin-right: var(--offset);
	text-decoration: none;
	font-weight: bold;
	padding: var(--offset-half);
}

.nav a:last-of-type {
	margin: 0;
}

/* .main {} */

.title {
	margin-bottom: var(--offset);
	text-align: center;
}

.controls {
	margin-bottom: var(--offset);
	border: 1px solid lightblue;
	border-radius: calc(var(--offset-half) / 2);
	padding: var(--offset);
}

.controls__field {
	margin-bottom: var(--offset-half);
	display: flex;
	flex-direction: column;
	align-items: flex-start;
}

.controls__field label {
	margin-bottom: calc(var(--offset-half) / 2);
}

.controls__field input {
	padding: 5px;
	min-width: 200px;
}

.controls__field select {
	min-width: 200px;
	padding: 5px;
}

.controls__button {
	margin-top: var(--offset);
}

.controls__button button {
	padding: 5px 10px;
}

.tablewrap {
	border: 1px solid lightblue;
	border-radius: calc(var(--offset-half) / 2);
	padding: var(--offset-half);
}
</style>
