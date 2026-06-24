// --- 1. Animation Redirect (Must be at the very top) ---
if (window.location.pathname.endsWith('index.html') || window.location.pathname === '/') {
    window.onload = () => {
        setTimeout(() => {
            window.location.href = '/welcome';
        }, 5000); 
    };
}

// --- 1. Video Loop (Onboarding Only) ---
const v1 = document.getElementById('v1'), v2 = document.getElementById('v2');
if (v1 && v2) {
    v1.play();
    v1.onended = () => { v1.style.display = 'none'; v2.style.display = 'block'; v2.play(); };
    v2.onended = () => { v2.style.display = 'none'; v1.style.display = 'block'; v1.currentTime = 0; v1.play(); };
}

// --- 2. Advanced Validation ---
let currentValidationId = 0; // Prevent race conditions

async function validate() {
    const input = document.getElementById('username');
    const btn = document.getElementById('nextBtn');
    const error = document.getElementById('error');
    const success = document.getElementById('success-msg');
    const val = input.value;

    const myId = ++currentValidationId; // Create unique ID for this specific call

    // Reset UI State
    btn.innerHTML = "Next";
    btn.disabled = true;
    error.style.display = 'none';
    success.style.display = 'none';

    if (val.length === 0) return;

    if (val.length < 3) {
        error.innerText = "Username is too short!";
        error.style.display = 'block';
        return;
    }

    btn.innerHTML = "Checking...";
    await new Promise(resolve => setTimeout(resolve, 800));

    // Exit if user started a new validation while we were waiting
    if (myId !== currentValidationId) return; 

    if (val.toLowerCase() === 'nox' || val.toLowerCase() === 'admin') {
        error.innerText = "This Username is Unfortunately Unavailable";
        error.style.display = 'block';
        btn.innerHTML = "Next";
    } else if (val.length > 15) {
        error.innerText = "Username too long!";
        error.style.display = 'block';
        btn.innerHTML = "Next";
    } else {
        success.innerText = val + "@nox is valid. You can take this.";
        success.style.display = 'block';
        btn.innerHTML = "Next";
        btn.disabled = false;
    }
}

// --- 3. UI Navigation ---
function nextStep(id) {
    document.querySelectorAll('.step').forEach(s => s.style.display = 'none');
    document.getElementById(id).style.display = 'block';
}
function validateName() {
    const input = document.getElementById('realname');
    const btn = document.getElementById('nextBtn2');
    const success = document.getElementById('name-success');
    
    const val = input.value.trim();
    const firstName = val.split(' ')[0];

    // If the input is empty, disable the button
    if (val.length < 2) {
        btn.disabled = true;
        success.style.display = 'none';
        return;
    }

    // Otherwise, show success message and enable button
    success.innerText = "We will call you " + firstName +  ".";
    success.style.display = 'block';
    btn.disabled = false;
}
// Populate Days and Years
const daySelect = document.getElementById('day');
const yearSelect = document.getElementById('year');

for (let i = 1; i <= 31; i++) daySelect.innerHTML += `<option value="${i}">${i}</option>`;
const currentYear = new Date().getFullYear();
for (let i = currentYear; i >= 1950; i--) yearSelect.innerHTML += `<option value="${i}">${i}</option>`;

function validateDOB() {
    const d = document.getElementById('day').value;
    const m = document.getElementById('month').value;
    const y = document.getElementById('year').value;
    const btn = document.getElementById('nextBtn3');
    const msg = document.getElementById('age-msg');

    if (d && m && y) {
        const birthDate = new Date(y, m - 1, d);
        const age = Math.floor((new Date() - birthDate) / 31557600000); // Rough age calc
        
        msg.innerText = `You are ${age} years old.`;
        msg.style.display = 'block';
        btn.disabled = false;
    }
}
// Toggle password visibility
function togglePassword() {
    const p = document.getElementById('password'), e = document.getElementById('toggle-eye');
    p.type = (p.type === 'password') ? 'text' : 'password';
    e.innerText = (p.type === 'text') ? '🙈' : '👁️';
}

// Password validation
function validatePassword() {
    const p = document.getElementById('password').value;
    const b = document.getElementById('nextBtn4');
    const e = document.getElementById('pass-error');
    
    if (p.length < 8) {
        e.style.display = 'block';
        e.innerText = "Password must be at least 8 characters.";
        b.disabled = true;
    } else {
        e.style.display = 'none';
        b.disabled = false;
    }
}
