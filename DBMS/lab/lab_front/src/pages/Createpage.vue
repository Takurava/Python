<template>
	<h1 class="title">Создать новые записи</h1>

	<div class="create_menu">
		<button @click="selectedMenuItem = 1">Добавить квартиру</button>
		<button @click="selectedMenuItem = 2">Добавить начисление</button>
		<button @click="selectedMenuItem = 3">Добавить платеж</button>
	</div>

	<div class="create_wrap">
		<div v-if="selectedMenuItem === 1" class="flat">
			<div class="controls">
				<div class="controls__field">
					<label for="newFlat">Введите номер новой квартиры</label>
					<input
						v-model="newFlat"
						type="number"
						required
						name="newflat"
						id="newFlat"
						placeholder="Введите квартиру"
					/>
				</div>

				<div class="controls__button">
					<button @click="createFlat">Создать квартиру</button>
				</div>
			</div>
		</div>

		<div v-if="selectedMenuItem === 2" class="flat">
			<div class="controls">
				<div class="controls__field">
					<label for="flat">Выберите квартиру</label>
					<select v-model="selectedFlat" required name="flat" id="flat">
						<option value="Выберите квартиру" selected>Выберите квартиру</option>
						<option v-for="flat in flats" :value="flat" :key="flat">{{ flat }}</option>
					</select>
				</div>

				<div class="controls__field">
					<label for="newCharge">Введите сумму начисления</label>
					<input
						v-model="newCharge"
						type="number"
						required
						name="newCharge"
						id="newCharge"
						placeholder="Введите начисление"
					/>
				</div>

				<div class="controls__button">
					<button @click="createCharge">Добавить начисление</button>
				</div>
			</div>
		</div>

		<div v-if="selectedMenuItem === 3" class="flat">
			<div class="controls">
				<div class="controls__field">
					<label for="flat">Выберите квартиру</label>
					<select v-model="selectedFlat" required name="flat" id="flat">
						<option value="Выберите квартиру" selected>Выберите квартиру</option>
						<option v-for="flat in flats" :value="flat" :key="flat">{{ flat }}</option>
					</select>
				</div>

				<div class="controls__field">
					<label for="newDate">Введите дату платежа</label>
					<input
						v-model="newDate"
						type="date"
						required
						name="newDate"
						id="newDate"
						placeholder="Введите сумму платежа"
					/>
				</div>

				<div class="controls__field">
					<label for="newPayment">Введите сумму платежа</label>
					<input
						v-model="newPayment"
						type="number"
						required
						name="newPayment"
						id="newPayment"
						placeholder="Введите сумму платежа"
					/>
				</div>

				<div class="controls__field">
					<h4>
						Начисление на
						{{ new Date().toLocaleDateString("ru-RU") }}
					</h4>
				</div>

				<div class="controls__button">
					<button @click="createPayment">Добавить начисление</button>
				</div>
			</div>
		</div>
	</div>

	<!-- <div class="tablewrap">{{ flats }}</div> -->
</template>

<script setup>
// Кнопка - добавить квартиру
// Ввести номер квартиры

// Кнопка - добавить начисление
// Ввести номер квартиры (выпадающий список)
// Дата (отображается дата сегодняшнего дня) 
// Ввести сумму начисления 

// Кнопка - добавить платеж
// Ввести номер квартиры (выпадающий список)
// Ввести дату 
// Ввести сумму платежа

import { ref, onBeforeMount } from "vue"
const flats = ref({})
const selectedMenuItem = ref(1)
const newFlat = ref()
const selectedFlat = ref("Выберите квартиру")
const newCharge = ref(0)
const newPayment = ref(0)
const newDate = ref(new Date())

onBeforeMount(() => {
	fetch(`http://127.0.0.1:5000/flat/all`, {
		method: "GET"
	})
		.then(res => res.json())
		.then(d => {
			flats.value = d
		})
		.catch(err => console.error(err))
})

const createFlat = () => {
	console.log(newFlat.value);
	console.log("try create flat");

	fetch("http://127.0.0.1:5000/flat", {
		method: "POST",
		headers: {
			'Accept': 'application/json',
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ 'flat_number': newFlat.value })
	})
		.then(res => res.json())
		.then(d => {
			console.log(d);
		})
		.catch(err => console.error(err))
}

const createCharge = () => {
	console.log(newCharge.value, selectedFlat.value);
	console.log("try create charge");

	fetch("http://127.0.0.1:5000/charge", {
		method: "POST",
		headers: {
			'Accept': 'application/json',
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ 'flat_number': selectedFlat.value, 'amount': newCharge.value })
	})
		.then(res => res.json())
		.then(d => {
			console.log(d);
		})
		.catch(err => console.error(err))
}

const createPayment = () => {
	console.log(newPayment.value, selectedFlat.value);
	const d = new Date(newDate.value)
	const year = d.getFullYear()
	const month = d.getMonth() + 1
	const day = d.getDate()

	fetch("http://127.0.0.1:5000/payment", {
		method: "POST",
		headers: {
			'Accept': 'application/json',
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			'flat_number': selectedFlat.value,
			'amount': newPayment.value,
			year: year,
			month: month,
			day: day
		})
	})
//		.then(res => res.json())
		.then(d => {
			console.log(d);
		})
		.catch(err => console.error(err))
}
</script>

<style>
.create_menu {
	display: flex;
	justify-content: center;
	margin-bottom: var(--offset);
}

.create_menu button {
	margin: 0 var(--offset-half);
	padding: 5px 10px;
}
</style>