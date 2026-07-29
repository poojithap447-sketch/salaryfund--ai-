import { useEffect, useRef } from 'react'
import gsap from 'gsap'

export default function AnimatedCounter({ value, duration = 1.6, decimals = 0, prefix = '', suffix = '', className }) {
  const ref = useRef(null)

  useEffect(() => {
    const el = ref.current
    const obj = { val: 0 }
    const tween = gsap.to(obj, {
      val: value,
      duration,
      ease: 'power2.out',
      onUpdate: () => {
        if (el) el.textContent = `${prefix}${obj.val.toFixed(decimals)}${suffix}`
      },
    })
    return () => tween.kill()
  }, [value, duration, decimals, prefix, suffix])

  return <span ref={ref} className={className}>{prefix}0{suffix}</span>
}
