<template>
	<h1 class="title">Оборотная ведомость</h1>

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

		<div class="controls__button">
			<button @click="sendRequest">Рассчитать</button>
		</div>
	</div>

	<div v-if="data.length > 0" class="tablewrap">
		<div class="tablehead">
			<div>Квартира</div>
			<div>Входящее сальдо</div>
			<div>Январь</div>
			<div>Февраль</div>
			<div>Март</div>
			<div>Апрель</div>
			<div>Май</div>
			<div>Июнь</div>
			<div>Июль</div>
			<div>Август</div>
			<div>Сентябрь</div>
			<div>Октябрь</div>
			<div>Ноябрь</div>
			<div>Декабрь</div>
			<div>Исходящее сальдо</div>
		</div>

		<div class="tablebody">
			<div v-for="item in data" class="tablerow">
				<div class="allrows">{{ item.flat }}</div>
				<div class="allrows inpsaldo">{{ item['output-saldo'].toFixed(2) }}</div>

				<template v-for="month in item['monthly-information']">
					<div>{{ month.charge.toFixed(2) }}</div>
					<div>{{ month.payment.toFixed(2) }}</div>
					<div>{{ month.saldo.toFixed(2) }}</div>
				</template>

				<div class="allrows outsaldo">{{ item['input-saldo'].toFixed(2) }}</div>
			</div>
		</div>
	</div>
</template>

<script setup>
// Выбор Года
// Копка - рассчитать
// Появление таблички
import { ref, onBeforeMount } from "vue"
const data = ref({})
const selectedYear = ref(2021)

const sendRequest = () => {
	fetch(`http://127.0.0.1:5000/statement?year=${selectedYear.value}`, {
		method: "GET"
	})
		.then(res => res.json())
		.then(d => {
			data.value = d
		})
		.catch(err => console.error(err))
}

onBeforeMount(() => {
})

</script>

<style scoped>
.tablehead {
	display: grid;
	grid-template-columns: repeat(15, 1fr);
	gap: var(--offset-half);
	font-size: 0.9rem;
	margin-bottom: var(--offset-half);

	padding: var(--offset-half) 0;
	background-color: #fff;
	border-bottom: 1px solid #000;

	position: sticky;
	top: 0;
}

.tablebody {
}

.tablerow {
	display: grid;
	grid-template-columns: repeat(15, 1fr);
	grid-template-rows: repeat(3, 1fr);
	gap: var(--offset-half);
	font-size: 0.9rem;
	padding: var(--offset-half) 0;

	border: 1px solid lightgreen;
	margin-bottom: var(--offset-half);
}

.tablerow div:first-of-type {
	justify-self: center;
}

.tablerow .allrows {
	grid-row: 1/-1;
	align-self: center;
}

.tablerow .inpsaldo {
	grid-column: 2/3;
}

.tablerow .inpsaldo {
	grid-column: 15/-1;
}
</style>