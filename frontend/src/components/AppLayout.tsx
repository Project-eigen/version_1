import React from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { Users, ScanLine, Archive } from 'lucide-react'
import Header from './Header'
import FamilyPills from './FamilyPills'
import type { User } from '../types'

interface LayoutProps {
  children: React.ReactNode
  familyMembers: User[]
  activeMemberId: number
  onSelectMember: (id: number) => void
  inboxCount?: number
}

type NavTab = 'family' | 'cabinet' | 'scan'

export default function AppLayout({
  children,
  familyMembers,
  activeMemberId,
  onSelectMember,
  inboxCount = 0,
}: LayoutProps) {
  const navigate = useNavigate()
  const location = useLocation()
  const { user } = useAuth()

  const currentTab: NavTab =
    location.pathname.startsWith('/cabinet') ? 'cabinet'
    : location.pathname.startsWith('/scan') ? 'scan'
    : 'family'

  return (
    <>
      <Header inboxCount={inboxCount} />
      <FamilyPills
        members={familyMembers}
        activeMemberId={activeMemberId}
        onSelect={onSelectMember}
        currentUserId={user?.id ?? 0}
      />

      {/* Page content */}
      <div className="page-content">
        {children}
      </div>

      {/* Bottom Navigation */}
      <nav className="bottom-nav" role="navigation" aria-label="Main navigation">
        {/* Family Tab */}
        <button
          id="nav-family"
          className={`nav-item ${currentTab === 'family' ? 'active' : ''}`}
          onClick={() => navigate('/home')}
          aria-label="Family Settings"
        >
          <Users size={20} />
          <span>Family</span>
        </button>

        {/* Center Scan Button */}
        <button
          id="nav-scan"
          className="scan-nav-btn"
          onClick={() => navigate('/scan')}
          aria-label="Scan medicine"
        >
          <ScanLine size={26} color="white" strokeWidth={2.5} />
        </button>

        {/* Cabinet Tab */}
        <button
          id="nav-cabinet"
          className={`nav-item ${currentTab === 'cabinet' ? 'active' : ''}`}
          onClick={() => navigate('/cabinet')}
          aria-label="Cabinet"
        >
          <Archive size={20} />
          <span>Cabinet</span>
        </button>
      </nav>
    </>
  )
}
