<template>
	<h1 class="title">Начисления и платежи</h1>

	<div class="controls">
		<div class="controls__field">
			<label for="year">Выберите год</label>
			<input
				v-model="selectedYear"
				type="number"
				required
				name="year"
				id="year"
				placeholder="Введите год"
			/>
		</div>

		<div class="controls__field">
			<label for="flat">Выберите квартиру</label>
			<select v-model="selectedFlat" required name="flat" id="flat">
				<option value="Выберите квартиру" selected>Выберите квартиру</option>
				<option v-for="flat in flats" :value="flat" :key="flat">{{ flat }}</option>
			</select>
		</div>

		<div class="controls__button">
			<button @click="sendRequest">Рассчитать</button>
		</div>
	</div>

	<div v-if="Object.keys(data).length > 0" class="tablewrap">
		<div class="tablehead">
			<div>Начало года (+ долг / - переплата)</div>
			<div></div>
			<div>1</div>
			<div>2</div>
			<div>3</div>
			<div>4</div>
			<div>5</div>
			<div>6</div>
			<div>7</div>
			<div>8</div>
			<div>9</div>
			<div>10</div>
			<div>11</div>
			<div>12</div>
			<div>Итого</div>
			<div>+ долг / - переплата</div>
		</div>

		<div class="tablebody">
			<div class="tablerow">
				<div class="inputsaldo">{{ data['input-saldo'] }}</div>
				<div class="tworow">
					<div>Начисления</div>
					<div>Оплата</div>
				</div>

				<div class="tworow" v-for="item in data['monthly-information']">
					<div>{{ item.charge }}</div>
					<div>{{ item.payment }}</div>
				</div>

				<div class="tworow">
					<div>{{ data.total.charge.toFixed(2) }}</div>
					<div>{{ data.total.payment.toFixed(2) }}</div>
				</div>

				<div class="deltasaldo">{{ data['delta-saldo'].toFixed(2) }}</div>

				<div class="total_string">Итого к оплате:</div>
				<div class="total">{{ data['output-saldo'] }}</div>
			</div>
		</div>
	</div>
</template>

<script setup>
// Выбор Года
// Выбор Квартиры (выпадающий список)
// Копка - рассчитать
// Появление таблички
import { ref, onBeforeMount } from "vue"
const data = ref({})
const flats = ref([])

const selectedYear = ref(2021)
const selectedFlat = ref("Выберите квартиру")

const sendRequest = () => {
	console.log(selectedFlat.value, selectedYear.value);

	fetch(`http://127.0.0.1:5000/month?year=${selectedYear.value}&flat=${selectedFlat.value}`, {
		method: "GET"
	})
		.then(res => res.json())
		.then(d => {
			console.log("data", d);
			data.value = d
		})
		.catch(err => console.error(err))
}

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
</script>

<style scoped>
.tablehead {
	display: grid;
	grid-template-columns: 80px 100px repeat(14, 1fr);
	gap: var(--offset-half);
	font-size: 0.9rem;
	margin-bottom: var(--offset-half);

	padding: var(--offset-half) 0;
	background-color: #fff;
	border-bottom: 1px solid #000;

	position: sticky;
	top: 0;
	text-align: center;
}

.tablebody {
}

.tablerow {
	display: grid;
	grid-template-columns: 80px 100px repeat(14, 1fr);
	grid-template-rows: repeat(2, 1fr);
	gap: var(--offset-half);
	font-size: 0.9rem;
	padding: var(--offset-half) 0;

	border: 1px solid lightgreen;
	margin-bottom: var(--offset-half);

	text-align: center;
}

.tablerow .tworow div:first-of-type {
	margin-bottom: 10px;
}

.tablerow .inputsaldo {
	text-align: center;
}

.tablerow .total_string {
	grid-row: 2/3;
	grid-column: 1/-2;
	text-align: right;
}

.tablerow .deltasaldo {
	grid-row: 1/2;
	grid-column: -2/-1;
}

.tablerow .total {
	grid-row: 2/3;
}
</style>