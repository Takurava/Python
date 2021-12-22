<template>
	<h1 class="title">Должники по категориям</h1>
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
			<select v-model="selectedMonth" required name="flat" id="flat">
				<option value="Выберите месяц" selected>Выберите месяц</option>
				<option value="1">Январь</option>
				<option value="2">Февраль</option>
				<option value="3">Март</option>
				<option value="4">Апрель</option>
				<option value="5">Май</option>
				<option value="6">Июнь</option>
				<option value="7">Июль</option>
				<option value="8">Август</option>
				<option value="9">Сентябрь</option>
				<option value="10">Октябрь</option>
				<option value="11">Ноябрь</option>
				<option value="12">Декабрь</option>
			</select>
		</div>

		<div class="controls__button">
			<button @click="sendRequest">Рассчитать</button>
		</div>
	</div>

	<div v-if="data.length > 0" class="tablewrap">
		<div class="tablehead">
			<div class="flat">Квартира</div>
			<div class="last_month">Начислено за последний месяц</div>
			<div class="saldo">Сальдо</div>
			<div class="dolg">Задолженность</div>
			<div class="periods">
				<div class="period1">1 месяц</div>
				<div class="period2">2 месяца</div>
				<div class="period3">3 месяца</div>
				<div class="period4">Свыше 3-х месяцев</div>
			</div>
		</div>

		<div class="tablebody">
			<div v-for="item in data" class="tablerow">
				<div class>{{ item.flat }}</div>
				<div class>{{ item['last-month-charge'] }}</div>
				<div class>{{ item.saldo }}</div>

				<template v-for="appear in item.arrears">
					<div>{{ appear }}</div>
				</template>
			</div>
		</div>
	</div>
</template>

<script setup>
// Выбор Года
// Выбор Месяца
// Копка - рассчитать
// Появление таблички
import { ref, onBeforeMount } from "vue"
const data = ref({})

const selectedYear = ref(2021)
const selectedMonth = ref("Выберите месяц")

const sendRequest = () => {
	console.log(selectedMonth.value, selectedYear.value);

	fetch(`http://127.0.0.1:5000/debtors?year=${selectedYear.value}&month=${selectedMonth.value}&day=01`, {
		method: "GET"
	})
		.then(res => res.json())
		.then(d => {
			console.log(d);
			data.value = d
		})
		.catch(err => console.error(err))
}
</script>

<style scoped>
.tablehead {
	display: grid;
	grid-template-columns: 120px 1fr 200px 3fr;
	grid-template-rows: repeat(2, 1fr);
	gap: var(--offset-half);
	font-size: 0.9rem;
	margin-bottom: var(--offset-half);

	padding: var(--offset-half) 0;
	background-color: #fff;
	border-bottom: 1px solid #000;

	position: sticky;
	top: 0;
}

.tablehead .flat {
	grid-row: 1/3;
}

.tablehead .last_month {
	grid-row: 1/3;
}

.tablehead .saldo {
	grid-row: 1/3;
}

.tablehead .dolg {
	text-align: center;
	grid-row: 1/2;
}

.tablehead .periods {
	grid-row: 2/3;
	grid-column: 4/-1;

	display: grid;
	grid-template-columns: repeat(4, 1fr);
	gap: var(--offset-half);
}

.tablebody {
}

.tablerow {
	display: grid;
	grid-template-columns: 120px 245px 200px repeat(4, 1fr);
	gap: var(--offset-half);
	border: 1px solid lightgreen;
	margin-bottom: var(--offset-half);
	padding: 5px;
}
</style>