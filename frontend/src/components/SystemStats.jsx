import React, { useEffect, useState } from 'react'
import { Cpu, HardDrive, Zap } from 'lucide-react'
import { systemService } from '../services/api'

function SystemStats() {
  const [stats, setStats] = useState({
    cpu_percent: 0,
    memory_percent: 0,
    battery_percent: 0,
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadStats()
    const interval = setInterval(loadStats, 5000)
    return () => clearInterval(interval)
  }, [])

  const loadStats = async () => {
    try {
      const data = await systemService.getStats()
      setStats(data)
      setLoading(false)
    } catch (error) {
      console.error('Failed to load stats:', error)
    }
  }

  const StatCard = ({ icon: Icon, label, value, unit }) => (
    <div className="glass rounded-lg p-3 text-center">
      <Icon size={20} className="text-aji-accent mx-auto mb-2" />
      <div className="text-xs text-gray-400">{label}</div>
      <div className="text-lg font-semibold text-white">
        {value}<span className="text-sm text-gray-400">{unit}</span>
      </div>
    </div>
  )

  if (loading) return <div>Loading...</div>

  return (
    <>
      <StatCard icon={Cpu} label="CPU" value={stats.cpu_percent?.toFixed(1)} unit="%" />
      <StatCard icon={HardDrive} label="Memory" value={stats.memory_percent?.toFixed(1)} unit="%" />
      <StatCard icon={Zap} label="Battery" value={stats.battery_percent?.toFixed(0)} unit="%" />
    </>
  )
}

export default SystemStats
