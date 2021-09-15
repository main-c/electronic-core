var nav = document.querySelector('.nav')
var navbar = document.querySelector('.navbar')


window.addEventListener('scroll',()=>{

	if(window.scrollY > 100){

		nav.classList.add('navScroll')
	}
	else {
		nav.classList.remove('navScroll')
	}
});