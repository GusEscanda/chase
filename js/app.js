const fieldWrapper = document.querySelector('.field-wrapper');
const field = document.getElementById('field');
const instructions = document.getElementById('instructions');
const pressToEnter = document.getElementById('pressToEnter');
const gameTitleScreen = document.getElementById('gameTitleScreen');
const newGameButton = document.getElementById('new');
const fieldWidth = field.offsetWidth;

loadDimensions = () => {
  window.innerWidth < window.innerHeight ? fieldWrapper.style.height = claculateDimension(22, 26) : fieldWrapper.style.height = claculateDimension(26, 22);
  console.log('fieldWidth', fieldWidth);
  console.log(fieldWrapper.offsetHeight);
  console.log('Relación: ', fieldWidth * 22 / 26);
}

loadChaseScreenInteraction = () => {
  if (gameTitleScreen.classList.contains('game-title--active')) {
    console.log('loadChaseScreenInteraction');
    window.addEventListener('keydown', e => {
      removeGameTitleScreen();
    });
    window.addEventListener('click', e => {
      removeGameTitleScreen();
    });
    setTimeout(() => {
      pressToEnter.classList.add('game-title__press-to-enter--active');
    }, 3000);
  }
}

removeGameTitleScreen = () => {
  gameTitleScreen.style.transition = 'none';
  gameTitleScreen.classList.remove('game-title--active');
}

claculateDimension = (d1, d2) => {
  return `${(fieldWidth / d1) * d2}px`;
}

retainScroll = () => {
  window.addEventListener("keydown", e => {
    if(["Space","ArrowUp","ArrowDown","ArrowLeft","ArrowRight"].indexOf(e.code) > -1) {
        e.preventDefault();
    }
  }, false);
}

openInstructions = () => {
  if (!instructions.classList.contains('instructions--active')) {
    instructions.classList.add('instructions--active');
  }
}

closeInstructions = () => {
  if (instructions.classList.contains('instructions--active')) {
    instructions.classList.remove('instructions--active');
  }
}

// console.log('------------------------------------------------>');
loadDimensions();
loadChaseScreenInteraction();
retainScroll();
// console.log('------------------------------------------------>');
