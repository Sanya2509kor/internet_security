document.getElementById('quiz-form').addEventListener('submit', (e) => {
  e.preventDefault();
  let correct = 0, total = 0;

  document.querySelectorAll('.quiz-item').forEach(item => {
    total++;
    const correctIdx = item.dataset.correct;
    const selected = item.querySelector('input:checked');

    item.querySelectorAll('.answer').forEach(a => a.classList.remove('correct', 'wrong'));

    if (selected) {
      const label = selected.closest('.answer');
      if (selected.value === correctIdx) {
        label.classList.add('correct');
        correct++;
      } else {
        label.classList.add('wrong');
        // подсветить правильный
        const answers = item.querySelectorAll('.answer');
        answers[correctIdx].classList.add('correct');
      }
    } else {
      const answers = item.querySelectorAll('.answer');
      answers[correctIdx].classList.add('correct');
    }

    const exp = item.querySelector('.explanation');
    if (exp) exp.hidden = false;
  });

  const res = document.getElementById('result');
  res.hidden = false;
  const percent = Math.round((correct / total) * 100);
  let msg = percent === 100 ? '🏆 Отлично! Ты настоящий эксперт по безопасности!'
           : percent >= 70 ? '👍 Хорошо! Но есть что подучить.'
           : '📚 Неплохо для начала — прочитай материалы и попробуй снова!';
  res.innerHTML = `Правильных ответов: <strong>${correct} из ${total} (${percent}%)</strong><br>${msg}`;
  res.scrollIntoView({ behavior: 'smooth', block: 'center' });
});