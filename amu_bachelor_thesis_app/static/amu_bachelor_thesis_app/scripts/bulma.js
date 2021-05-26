const navbarBurgers = Array.from(document.querySelectorAll('.navbar-burger'));
if(navbarBurgers.length > 0) {
    navbarBurgers.forEach(burger => {
       burger.addEventListener('click', () => {
           const target = burger.dataset.target;
           burger.classList.toggle('is-active');
           document.getElementById(target).classList.toggle('is-active');
       });
    });
}