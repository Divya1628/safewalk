document.addEventListener('DOMContentLoaded', () => {
  const signInBtn = document.querySelector('.sign-in-btn');
  const demoBtn = document.querySelector('.demo-access-btn');

  const showDashboard = () => {
    document.body.classList.add('dashboard-view');
  };

  if (signInBtn) {
    signInBtn.addEventListener('click', showDashboard);
  }

  if (demoBtn) {
    demoBtn.addEventListener('click', showDashboard);
  }
});
