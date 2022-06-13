$(document).on('click',".subj", function(){
	if($(this).children('button').length === 0){
		const hr = document.createElement('hr');
		hr.setAttribute("id","sep");
		hr.setAttribute("style","display:none");
		$(this).append(hr);

		const task = document.createElement('button');
		const task_img = document.createElement('img');
		task_img.setAttribute('src', './media/add.svg');

		task.appendChild(task_img);
		task.setAttribute('style', 'color:blue');
		task.append("Добавить задание");
		$(this).append(task);

		const chg = document.createElement('button');
		const chg_img = document.createElement('img');
		chg_img.setAttribute('src', './media/add.svg');

		chg.appendChild(chg_img);
		chg.setAttribute('style', 'color:green');
		chg.append("Перенести пару");
		$(this).append(chg);

		const cnl = document.createElement('button');
		const cnl_img = document.createElement('img');
		cnl_img.setAttribute('src', './media/add.svg');

		cnl.appendChild(cnl_img);
		cnl.setAttribute('style', 'color:red');
		cnl.append("Отменить пару");
		$(this).append(cnl);

		$(this).children('button').css("display", "none");
	}

	$(this).children('#sep, #prep').toggle("slow");
	$(this).children('button').toggle("slow");

	const line = $(this).children('div').children('p');

	if(line.is(':empty')){
		if($(this).hasClass("lab")) line.append("Лабораторная");
		else if ($(this).hasClass("lect")) line.append("Лекция");
		else if ($(this).hasClass("pract")) line.append("Практика");
		else if ($(this).hasClass("other")) line.append("Прочее");
	}
	line.toggle("slow");
})