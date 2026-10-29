const viewer = document.querySelector('.viewer');
let gallery = [];
let activeIndex = 0;
let trigger;
function showImage(index) {
  activeIndex = (index + gallery.length) % gallery.length;
  const button = gallery[activeIndex];
  const image = button.querySelector('img');
  const enlarged = document.querySelector('#viewer-image');
  enlarged.src = image.getAttribute('src');
  enlarged.alt = image.alt;
  document.querySelector('#viewer-title').textContent = button.dataset.title;
  document.querySelector('#viewer-original').href = image.getAttribute('src');
  document.querySelector('#viewer-count').textContent = `${activeIndex + 1} of ${gallery.length}`;
  document.querySelector('#viewer-prev').disabled = gallery.length < 2;
  document.querySelector('#viewer-next').disabled = gallery.length < 2;
  document.querySelector('.viewer-body').scrollTop = 0;
}
document.querySelectorAll('.image-button').forEach(button => {
  button.addEventListener('click', () => {
    trigger = button;
    gallery = [...document.querySelectorAll('.image-button')].filter(b => b.dataset.gallery === button.dataset.gallery);
    showImage(gallery.indexOf(button));
    viewer.showModal();
    document.body.classList.add('viewer-open');
    document.querySelector('#viewer-close').focus();
  });
});
document.querySelector('#viewer-close').addEventListener('click', () => viewer.close());
document.querySelector('#viewer-prev').addEventListener('click', () => showImage(activeIndex - 1));
document.querySelector('#viewer-next').addEventListener('click', () => showImage(activeIndex + 1));
viewer.addEventListener('close', () => {
  document.body.classList.remove('viewer-open');
  trigger?.focus();
});
viewer.addEventListener('keydown', event => {
  if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
    event.preventDefault();
    showImage(activeIndex + (event.key === 'ArrowRight' ? 1 : -1));
  }
});
// Native disclosure and direct links keep project browsing usable without JavaScript.
