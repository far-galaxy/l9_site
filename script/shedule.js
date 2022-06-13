const sheduleContainer = $(".rasp");

const cleanContainer = () => 
{
	sheduleContainer.empty();
}

window.onload = fetch("shedule.json")
	.then(response => response.json())
	.then(json => {
	makeShedule(json.shedule);
});

const makeShedule = (shedule) => 
{

	cleanContainer();
	
	sheduleContainer.append(`<div class="head">Время</div>
			<div class="head">пн</div>
			<div class="head">вт</div>
			<div class="head">ср</div>
			<div class="head">чт</div>
			<div class="head">пт</div>
			<div class="head">сб</div>`);

	sheduleContainer.append('<div class="time">08:00<hr>09:35</div>');

	shedule.map(data => buildCard(data)).forEach(node => sheduleContainer.append(node));
}

const buildCard = (data) => 
{
	const card = document.createElement('div');
	card.classList.add("subj");

	if (data.length === 1)
		{
		lesson = data[0];
		if (lesson.type){
			card.classList.add(lesson.type);
			card.innerHTML = `<div><p></p></div>
			<h2>${lesson.name}<\h2>
			<hr>
			<h5 id="prep">${lesson.teacher}</h5>
			<h3>${lesson.place}</h3>
			`;
		}
	}
	else if (data.length === 2 && data[0].name === data[1].name)
		{
			card.classList.add(data[0].type);
			card.innerHTML = `<div><p></p></div>
			<h2>${data[0].name}<\h2>
			<hr>
			<h5>${data[0].group}</h5>
			<h5 id="prep">${data[0].teacher}</h5>
			<h3>${data[0].place}</h3>
			<hr>
			<h5>${data[1].group}</h5>
			<h5 id="prep">${data[1].teacher}</h5>
			<h3>${data[1].place}</h3>
			`;
		}
	else if (data.length === 2 && data[0].name != data[1].name)
		{
			//TODO: make this stuff later
		}
	else
		{
			//TODO: Holy shit, and most importantly - why?
		}
	return card;
}