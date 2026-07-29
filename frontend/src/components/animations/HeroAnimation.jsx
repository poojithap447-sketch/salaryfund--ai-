import { useEffect, useRef } from 'react'
import gsap from 'gsap'

export default function HeroAnimation({ children }) {
  const scope = useRef(null)

  useEffect(() => {
    const ctx = gsap.context(() => {
      const tl = gsap.timeline({ defaults: { ease: 'power3.out' } })
      tl.fromTo('[data-hero-eyebrow]', { opacity: 0, y: -12 }, { opacity: 1, y: 0, duration: 0.6 })
        .fromTo('[data-hero-title] span', { opacity: 0, y: 28 }, { opacity: 1, y: 0, duration: 0.7, stagger: 0.06 }, '-=0.3')
        .fromTo('[data-hero-sub]', { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.6 }, '-=0.35')
        .fromTo('[data-hero-cta]', { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.6, stagger: 0.08 }, '-=0.35')
        .fromTo('[data-hero-panel]', { opacity: 0, scale: 0.94, y: 24 }, { opacity: 1, scale: 1, y: 0, duration: 0.9 }, '-=0.5')

      gsap.to('[data-hero-orb]', {
        y: -18,
        x: 12,
        duration: 6,
        repeat: -1,
        yoyo: true,
        ease: 'sine.inOut',
        stagger: { each: 0.8, from: 'random' },
      })
    }, scope)

    return () => ctx.revert()
  }, [])

  return <div ref={scope}>{children}</div>
}
