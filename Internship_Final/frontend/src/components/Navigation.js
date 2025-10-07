import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { BookOpen, MessageCircle } from 'lucide-react';

const Navigation = () => {
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Audiobook Generator', icon: BookOpen },
    { path: '/chat', label: 'AI Assistant', icon: MessageCircle }
  ];

  return (
    <nav className="nav">
      <div className="container">
        <div className="nav-content">
          <div className="nav-brand" sttyle>
            <BookOpen size={24} />
            <span><span style={{background: 'linear-gradient(135deg, #3b82f6, #8b5cf6)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent'}}>Expl</span><span style={{color: '#ff6b35', fontWeight: 'bold'}}>AI</span><span style={{background: 'linear-gradient(135deg, #3b82f6, #8b5cf6)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent'}}>nia</span></span>
          </div>

          <div className="nav-links">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`nav-link ${isActive ? 'active' : ''}`}
                >
                  <Icon size={16} />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;