<!-- Sidebar -->
<!-- <script>
    document.querySelector('.logout-btn').addEventListener('click', () => {
        localStorage.removeItem('user_token');
    });
</script> -->

<head>
    <link rel="stylesheet" href="styles/nav.css">
</head>
<div class="sidebar">
    <div id="user-profile-section" class="user-profile">
        <span id="welcome" class="welcome-text">Welkom, </span>
        <span id="display-name" class="user-name"></span>
        <span id="admin-label" class="user-role-badge hidden">Admin</span>
    </div>
    <div>
        <!-- <h2>Dashboard</h2> -->
        <div class="nav-links"></div>
    </div>
    <a href="/logout.php" class="logout-btn">Log uit</a>
</div>
<script>
    document.addEventListener('DOMContentLoaded', () => {
        const token = localStorage.getItem('user_token');

        // Redirect if no token found
        if (!token) {
            window.location.href = '/auth';
            return;
        }

        // Helper to decode JWT
        function parseJwt(token) {
            try {
                return JSON.parse(atob(token.split('.')[1]));
            } catch (e) {
                return null;
            }
        }

        const decoded = parseJwt(token);
        if (!decoded || !decoded.user_id) {
            localStorage.removeItem('user_token');
            window.location.href = '/auth';
            return;
        }

        fetch(`http://localhost:8001/get_user_pages/${decoded.user_id}`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        })
        .then(response => response.json())
        .then(pages => {
            const navLinks = document.querySelector('.nav-links');
            navLinks.innerHTML = '';
            pages['pages'].forEach(page => {
                const link = document.createElement('a');
                link.href = page.link;
                link.textContent = page.name;
                navLinks.appendChild(link);
            });
        })
        .catch(err => console.error('Error loading user pages:', err));

        fetch(`http://localhost:8001/get_user_details/${decoded.user_id}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Display Name
                    document.getElementById('display-name').textContent = data.user.name;

                    // Show Admin Label if admin
                    if (data.success) {
                        // Display Name
                        document.getElementById('display-name').textContent = data.user.name;

                        // Show Admin Label if admin and hide Laadpalen page for non admins
                        const isAdmin = data.user.role && data.user.role.toLowerCase() === 'admin';
                        if (isAdmin) {
                            document.getElementById('admin-label').classList.remove('hidden');
                            document.getElementById('laadpalen-link').classList.remove('hidden');
                        } else {
                            document.getElementById('admin-label').classList.add('hidden');
                            document.getElementById('laadpalen-link').classList.add('hidden');
                        }
                    }
                }
            })
            .catch(err => console.error('Error loading user:', err));

        // Logout Button
        const logoutBtn = document.querySelector('.logout-btn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', (e) => {
                e.preventDefault();
                localStorage.removeItem('user_token');
                window.location.href = '/logout.php';
            });
        }
    });
</script>