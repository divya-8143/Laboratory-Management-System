'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { User, RoleType } from '@/types';
import { apiClient } from './api-client';

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<User>;
  logout: () => void;
  isLoading: boolean;
  hasRole: (roles: RoleType[]) => boolean;
  switchRoleDemo: (role: RoleType) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const storedToken = localStorage.getItem('lms_access_token');
    const storedUser = localStorage.getItem('lms_user');

    if (storedToken && storedUser) {
      setToken(storedToken);
      try {
        setUser(JSON.parse(storedUser));
      } catch (e) {
        localStorage.removeItem('lms_user');
      }
    }
    setIsLoading(false);
  }, []);

  const login = async (email: string, password: string): Promise<User> => {
    const res = await apiClient.post('/auth/login', { email, password });
    const { access_token, refresh_token, ...userData } = res.data;

    localStorage.setItem('lms_access_token', access_token);
    localStorage.setItem('lms_refresh_token', refresh_token);
    localStorage.setItem('lms_user', JSON.stringify(userData));

    setToken(access_token);
    setUser(userData as User);
    return userData as User;
  };

  const logout = () => {
    localStorage.removeItem('lms_access_token');
    localStorage.removeItem('lms_refresh_token');
    localStorage.removeItem('lms_user');
    setToken(null);
    setUser(null);
  };

  const hasRole = (roles: RoleType[]): boolean => {
    if (!user) return false;
    return roles.includes(user.role);
  };

  // Demo role switch helper for testing all role portals instantly
  const switchRoleDemo = async (role: RoleType) => {
    const creds: Record<RoleType, { e: string; p: string }> = {
      ADMIN: { e: 'admin@acupath.com', p: 'Admin@12345' },
      RECEPTIONIST: { e: 'reception@acupath.com', p: 'Reception@12345' },
      TECHNICIAN: { e: 'technician@acupath.com', p: 'Technician@12345' },
      DOCTOR: { e: 'doctor@acupath.com', p: 'Doctor@12345' },
      PATIENT: { e: 'john.doe@gmail.com', p: 'Patient@12345' },
    };

    const target = creds[role];
    if (target) {
      await login(target.e, target.p);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        login,
        logout,
        isLoading,
        hasRole,
        switchRoleDemo,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
