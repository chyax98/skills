/**
 * Presentation Navigation System
 * Handles keyboard, mouse, and touch navigation
 */

class Presentation {
  constructor() {
    this.currentSlide = 0;
    this.slides = document.querySelectorAll('.slide');
    this.totalSlides = this.slides.length;
    this.isFullscreen = false;

    this.controls = {
      prev: document.querySelector('.prev'),
      next: document.querySelector('.next'),
      fullscreen: document.querySelector('.fullscreen'),
      slideNumber: document.querySelector('.slide-number'),
      progressBar: document.querySelector('.progress-bar')
    };

    this.init();
  }

  init() {
    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
      switch(e.key) {
        case 'ArrowRight':
        case ' ':
        case 'PageDown':
          e.preventDefault();
          this.next();
          break;
        case 'ArrowLeft':
        case 'PageUp':
          e.preventDefault();
          this.prev();
          break;
        case 'Home':
          e.preventDefault();
          this.goToSlide(0);
          break;
        case 'End':
          e.preventDefault();
          this.goToSlide(this.totalSlides - 1);
          break;
        case 'f':
        case 'F':
          e.preventDefault();
          this.toggleFullscreen();
          break;
      }
    });

    // Mouse click navigation
    document.addEventListener('click', (e) => {
      if (e.target.closest('.controls')) return;

      const rect = window.innerWidth;
      const clickX = e.clientX;

      if (clickX < rect / 3) {
        this.prev();
      } else if (clickX > (rect * 2) / 3) {
        this.next();
      }
    });

    // Touch swipe navigation
    let touchStartX = 0;
    let touchEndX = 0;

    document.addEventListener('touchstart', (e) => {
      touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    document.addEventListener('touchend', (e) => {
      touchEndX = e.changedTouches[0].screenX;
      this.handleSwipe();
    }, { passive: true });

    // Button controls
    this.controls.prev.addEventListener('click', () => this.prev());
    this.controls.next.addEventListener('click', () => this.next());
    this.controls.fullscreen.addEventListener('click', () => this.toggleFullscreen());

    // Fullscreen change listener
    document.addEventListener('fullscreenchange', () => {
      this.isFullscreen = !!document.fullscreenElement;
      this.controls.fullscreen.textContent = this.isFullscreen ? '⛶' : '⛶';
    });

    // Initial render
    this.updateSlide();
  }

  handleSwipe() {
    const swipeThreshold = 50;
    const diff = touchStartX - touchEndX;

    if (Math.abs(diff) > swipeThreshold) {
      if (diff > 0) {
        this.next();
      } else {
        this.prev();
      }
    }
  }

  next() {
    if (this.currentSlide < this.totalSlides - 1) {
      this.currentSlide++;
      this.updateSlide();
    }
  }

  prev() {
    if (this.currentSlide > 0) {
      this.currentSlide--;
      this.updateSlide();
    }
  }

  goToSlide(index) {
    if (index >= 0 && index < this.totalSlides) {
      this.currentSlide = index;
      this.updateSlide();
    }
  }

  updateSlide() {
    // Update slide visibility
    this.slides.forEach((slide, index) => {
      slide.classList.remove('active', 'prev');

      if (index === this.currentSlide) {
        slide.classList.add('active');
      } else if (index < this.currentSlide) {
        slide.classList.add('prev');
      }
    });

    // Update controls
    this.updateControls();

    // Update progress
    this.updateProgress();

    // Trigger animations for active slide
    this.triggerAnimations();
  }

  updateControls() {
    // Disable/enable buttons
    this.controls.prev.disabled = this.currentSlide === 0;
    this.controls.next.disabled = this.currentSlide === this.totalSlides - 1;

    // Update slide number
    this.controls.slideNumber.textContent = `${this.currentSlide + 1} / ${this.totalSlides}`;
  }

  updateProgress() {
    const progress = ((this.currentSlide + 1) / this.totalSlides) * 100;
    this.controls.progressBar.style.width = `${progress}%`;
  }

  triggerAnimations() {
    const activeSlide = this.slides[this.currentSlide];
    const animatedElements = activeSlide.querySelectorAll('.animate-fade-in');

    // Reset animations
    animatedElements.forEach(el => {
      el.style.animation = 'none';
      // Force reflow
      el.offsetHeight;
      el.style.animation = null;
    });
  }

  toggleFullscreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(err => {
        console.error(`Error attempting to enable fullscreen: ${err.message}`);
      });
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen();
      }
    }
  }
}

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    new Presentation();
  });
} else {
  new Presentation();
}
