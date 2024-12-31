// Auto-submit form when filters change
document.querySelectorAll('.filter-form select').forEach(select => {
    select.addEventListener('change', () => {
        select.closest('form').submit();
    });
});

// Favorite button functionality with CSRF token
document.querySelectorAll('.favorite-btn').forEach(btn => {
    btn.addEventListener('click', async (e) => {
        e.preventDefault();
        e.stopPropagation();
        
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const carId = btn.dataset.carId;
        
        try {
            const response = await fetch(`/api/favorite/${carId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json',
                },
            });
            
            if (response.ok) {
                const icon = btn.querySelector('i');
                icon.classList.toggle('fas');
                icon.classList.toggle('far');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });
});

// Smooth hover effects
document.querySelectorAll('.car-card').forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.style.transform = 'translateY(-5px)';
    });
    
    card.addEventListener('mouseleave', () => {
        card.style.transform = 'translateY(0)';
    });
});

// Django message handling
document.addEventListener('DOMContentLoaded', function() {
    const messages = document.querySelectorAll('.flash-message');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 300);
        }, 5000);
    });
});

// Mobile menu handling
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const mobileMenu = document.querySelector('.mobile-menu');
    
    if (mobileMenuToggle && mobileMenu) {
        mobileMenuToggle.addEventListener('click', function() {
            this.classList.toggle('active');
            mobileMenu.classList.toggle('active');
            document.body.classList.toggle('menu-open');
        });
    }
}); 