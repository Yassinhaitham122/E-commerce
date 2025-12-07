import shoeBlue from '../assets/shoe-blue.jpg';
import './hero.css';

export default function Hero() {
  const scrollToProducts = () => {
    const el = document.getElementById('products-section');
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  return (
    <section className="hero">
      <div className="hero-inner">
        <div className="hero-left">
          <h1 className="hero-title">Jordan Royal — The Drop</h1>
          <p className="hero-sub">
            Limited edition. Spinning in the spotlight. Shop the look.
          </p>
          <button className="hero-cta" onClick={scrollToProducts}>
            Shop Now
          </button>
        </div>

        <div className="hero-right">
          <div className="shoe-wrap">
            <img className="shoe" src={shoeBlue} alt="Jordan Royal" />
          </div>
        </div>
      </div>
    </section>
  );
}
