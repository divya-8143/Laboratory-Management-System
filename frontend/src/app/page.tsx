'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/lib/auth-context';
import { apiClient } from '@/lib/api-client';
import {
  Patient,
  Test,
  Order,
  Sample,
  TestResult,
  LabReport,
  KPIOverview,
  MostRequestedTest,
  RevenueTrend,
  CategoryDistribution,
  AuditLogItem,
  RoleType,
} from '@/types';
import {
  Activity,
  Users,
  FlaskConical,
  FileSpreadsheet,
  ClipboardCheck,
  FileText,
  BarChart3,
  ShieldCheck,
  Search,
  Plus,
  CheckCircle2,
  AlertTriangle,
  Clock,
  Download,
  QrCode,
  LogOut,
  RefreshCw,
  Droplets,
  DollarSign,
  AlertCircle,
  Eye,
  Check,
  X,
  Stethoscope,
  Building2,
  Calendar,
  Phone,
  Mail,
  UserCheck,
} from 'lucide-react';

export default function LISApp() {
  const { user, token, login, logout, switchRoleDemo, hasRole, isLoading: authLoading } = useAuth();

  // Navigation State
  const [activeTab, setActiveTab] = useState<string>('reception');
  const [notification, setNotification] = useState<{ type: 'success' | 'error'; message: string } | null>(null);

  // Data States
  const [patients, setPatients] = useState<Patient[]>([]);
  const [catalog, setCatalog] = useState<Test[]>([]);
  const [orders, setOrders] = useState<Order[]>([]);
  const [samples, setSamples] = useState<Sample[]>([]);
  const [worklist, setWorklist] = useState<any[]>([]);
  const [reports, setReports] = useState<LabReport[]>([]);
  const [kpis, setKpis] = useState<KPIOverview | null>(null);
  const [mostRequested, setMostRequested] = useState<MostRequestedTest[]>([]);
  const [revenueTrends, setRevenueTrends] = useState<RevenueTrend[]>([]);
  const [auditLogs, setAuditLogs] = useState<AuditLogItem[]>([]);

  // Search & Filter States
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null);

  // Form Modals
  const [showNewPatientModal, setShowNewPatientModal] = useState(false);
  const [showNewOrderModal, setShowNewOrderModal] = useState(false);
  const [showResultEntryModal, setShowResultEntryModal] = useState<any | null>(null);
  const [showVerifyModal, setShowVerifyModal] = useState<LabReport | null>(null);
  const [showQrModal, setShowQrModal] = useState(false);
  const [qrVerifyHash, setQrVerifyHash] = useState('');
  const [qrVerifyResult, setQrVerifyResult] = useState<any | null>(null);

  // New Patient Form State
  const [patientForm, setPatientForm] = useState({
    first_name: '',
    last_name: '',
    date_of_birth: '1990-01-01',
    gender: 'MALE',
    blood_group: 'O+',
    phone: '',
    email: '',
    address: '',
    medical_history_notes: '',
  });

  // New Order Form State
  const [orderForm, setOrderForm] = useState({
    patient_id: '',
    referring_doctor: '',
    clinical_notes: '',
    priority: 'ROUTINE',
    selected_test_ids: [] as string[],
    discount_amount: 0,
  });

  // Result Entry State
  const [resultInputs, setResultInputs] = useState<Record<string, { numeric_value?: number; text_value?: string; notes?: string }>>({});
  
  // Verification State
  const [verifyComments, setVerifyComments] = useState('');
  const [verifyInterpretation, setVerifyInterpretation] = useState('');

  // Login form state
  const [loginEmail, setLoginEmail] = useState('admin@acupath.com');
  const [loginPassword, setLoginPassword] = useState('Admin@12345');
  const [loginError, setLoginError] = useState('');

  const showToast = (message: string, type: 'success' | 'error' = 'success') => {
    setNotification({ type, message });
    setTimeout(() => setNotification(null), 4000);
  };

  // Load clinical data on mount / user change
  const refreshData = async () => {
    try {
      if (!user) return;
      const [patRes, catRes, ordRes, sampRes, repRes, kpiRes] = await Promise.allSettled([
        apiClient.get('/patients?limit=50'),
        apiClient.get('/catalog/tests'),
        apiClient.get('/orders?limit=50'),
        apiClient.get('/samples/queue?limit=50'),
        apiClient.get('/reports?limit=50'),
        apiClient.get('/analytics/overview'),
      ]);

      if (patRes.status === 'fulfilled') setPatients(patRes.value.data.items || []);
      if (catRes.status === 'fulfilled') setCatalog(catRes.value.data || []);
      if (ordRes.status === 'fulfilled') setOrders(ordRes.value.data.items || []);
      if (sampRes.status === 'fulfilled') setSamples(sampRes.value.data || []);
      if (repRes.status === 'fulfilled') setReports(repRes.value.data || []);
      if (kpiRes.status === 'fulfilled') setKpis(kpiRes.value.data || null);

      // Role specific queries
      if (hasRole(['ADMIN', 'TECHNICIAN', 'DOCTOR'])) {
        const wlRes = await apiClient.get('/results/worklist');
        setWorklist(wlRes.data || []);
      }
      if (hasRole(['ADMIN', 'DOCTOR'])) {
        const [mrRes, trendRes] = await Promise.all([
          apiClient.get('/analytics/most-requested'),
          apiClient.get('/analytics/revenue-trends?period_type=daily'),
        ]);
        setMostRequested(mrRes.data || []);
        setRevenueTrends(trendRes.data || []);
      }
      if (hasRole(['ADMIN'])) {
        const auditRes = await apiClient.get('/audit/logs?limit=50');
        setAuditLogs(auditRes.data || []);
      }
    } catch (err: any) {
      console.error('Data refresh error:', err);
    }
  };

  useEffect(() => {
    if (user) {
      refreshData();
    }
  }, [user]);

  // Handle Login
  const handleLoginSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoginError('');
    try {
      await login(loginEmail, loginPassword);
      showToast('Logged in successfully');
    } catch (err: any) {
      setLoginError(err.response?.data?.detail || 'Authentication failed. Check credentials.');
    }
  };

  // Handle Patient Creation
  const handleCreatePatient = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await apiClient.post('/patients', patientForm);
      showToast(`Patient ${res.data.first_name} ${res.data.last_name} (${res.data.patient_code}) registered!`);
      setShowNewPatientModal(false);
      refreshData();
    } catch (err: any) {
      showToast(err.response?.data?.detail || 'Failed to register patient', 'error');
    }
  };

  // Handle Order Creation
  const handleCreateOrder = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!orderForm.patient_id || orderForm.selected_test_ids.length === 0) {
      showToast('Please select a patient and at least one clinical test', 'error');
      return;
    }
    try {
      const payload = {
        patient_id: orderForm.patient_id,
        referring_doctor: orderForm.referring_doctor,
        clinical_notes: orderForm.clinical_notes,
        priority: orderForm.priority,
        test_ids: orderForm.selected_test_ids,
        discount_amount: Number(orderForm.discount_amount) || 0,
      };
      const res = await apiClient.post('/orders', payload);
      showToast(`Order ${res.data.order_number} placed! Barcode tubes generated.`);
      setShowNewOrderModal(false);
      setOrderForm({
        patient_id: '',
        referring_doctor: '',
        clinical_notes: '',
        priority: 'ROUTINE',
        selected_test_ids: [],
        discount_amount: 0,
      });
      refreshData();
    } catch (err: any) {
      showToast(err.response?.data?.detail || 'Failed to place order', 'error');
    }
  };

  // Handle Sample Actions
  const handleSampleAction = async (sampleId: string, action: 'collect' | 'receive' | 'reject', reason?: string) => {
    try {
      if (action === 'collect') {
        await apiClient.post(`/samples/${sampleId}/collect`, { notes: 'Collected at phlebotomy station' });
        showToast('Specimen collected successfully');
      } else if (action === 'receive') {
        await apiClient.post(`/samples/${sampleId}/receive`);
        showToast('Specimen accessioned into laboratory');
      } else if (action === 'reject') {
        await apiClient.post(`/samples/${sampleId}/reject`, { reason: reason || 'Specimen hemolyzed/compromised' });
        showToast('Specimen rejected', 'error');
      }
      refreshData();
    } catch (err: any) {
      showToast(err.response?.data?.detail || 'Action failed', 'error');
    }
  };

  // Handle Result Batch Entry
  const handleBatchResultsSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!showResultEntryModal) return;

    try {
      const resultsArray = Object.entries(resultInputs).map(([paramId, data]) => ({
        parameter_id: paramId,
        numeric_value: data.numeric_value !== undefined && data.numeric_value !== null ? Number(data.numeric_value) : undefined,
        text_value: data.text_value,
        technician_notes: data.notes,
      }));

      await apiClient.post('/results/batch-entry', {
        order_item_id: showResultEntryModal.order_item_id,
        results: resultsArray,
      });

      showToast('Parameter results recorded and clinical reference flags evaluated!');
      setShowResultEntryModal(null);
      setResultInputs({});
      refreshData();
    } catch (err: any) {
      showToast(err.response?.data?.detail || 'Failed to enter results', 'error');
    }
  };

  // Handle Doctor Verification
  const handleVerifyReport = async () => {
    if (!showVerifyModal) return;
    try {
      await apiClient.post(`/reports/${showVerifyModal.id}/verify`, {
        pathologist_comments: verifyComments || 'All parameters evaluated. Findings correlate clinically.',
        clinical_interpretation: verifyInterpretation || 'Diagnostic profile within accepted clinical parameters.',
      });
      showToast(`Report ${showVerifyModal.report_number} verified and digitally signed! PDF compiled.`);
      setShowVerifyModal(null);
      setVerifyComments('');
      setVerifyInterpretation('');
      refreshData();
    } catch (err: any) {
      showToast(err.response?.data?.detail || 'Failed to verify report', 'error');
    }
  };

  // Handle Public QR Verification
  const handleVerifyQr = async () => {
    if (!qrVerifyHash) return;
    try {
      const res = await apiClient.get(`/reports/public/verify/${qrVerifyHash.trim()}`);
      setQrVerifyResult(res.data);
    } catch (err: any) {
      setQrVerifyResult({ error: 'Invalid or unrecognized report verification hash token.' });
    }
  };

  // If not logged in, show Auth Gate
  if (!user && !authLoading) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center p-4">
        <div className="max-w-md w-full bg-slate-800 border border-slate-700 rounded-2xl shadow-2xl p-8 text-white">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-3 bg-sky-600 rounded-xl">
              <FlaskConical className="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight">AcuPath Diagnostics</h1>
              <p className="text-xs text-slate-400">Enterprise Laboratory Information System</p>
            </div>
          </div>

          <form onSubmit={handleLoginSubmit} className="space-y-4">
            {loginError && (
              <div className="p-3 bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs rounded-lg flex items-center gap-2">
                <AlertCircle className="w-4 h-4 shrink-0" />
                <span>{loginError}</span>
              </div>
            )}
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Email Address</label>
              <input
                type="email"
                value={loginEmail}
                onChange={(e) => setLoginEmail(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-sky-500"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Password</label>
              <input
                type="password"
                value={loginPassword}
                onChange={(e) => setLoginPassword(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-sky-500"
                required
              />
            </div>
            <button
              type="submit"
              className="w-full py-2.5 bg-sky-600 hover:bg-sky-500 font-semibold rounded-lg text-sm transition-colors shadow-lg shadow-sky-600/30"
            >
              Sign In to Laboratory Portal
            </button>
          </form>

          <div className="mt-8 pt-6 border-t border-slate-700">
            <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">
              One-Click Role Demonstration Access:
            </p>
            <div className="grid grid-cols-2 gap-2">
              {(['ADMIN', 'RECEPTIONIST', 'TECHNICIAN', 'DOCTOR', 'PATIENT'] as RoleType[]).map((r) => (
                <button
                  key={r}
                  onClick={() => switchRoleDemo(r)}
                  className="px-2.5 py-1.5 bg-slate-700/60 hover:bg-slate-700 text-xs font-medium rounded-lg text-slate-200 border border-slate-600/50 transition-all text-left flex items-center justify-between"
                >
                  <span>{r}</span>
                  <UserCheck className="w-3.5 h-3.5 text-sky-400" />
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900">
      {/* Top Banner & Header */}
      <header className="bg-slate-900 text-white sticky top-0 z-30 shadow-md border-b border-slate-800">
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-sky-600 rounded-lg">
              <FlaskConical className="w-6 h-6 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-bold tracking-tight text-lg">AcuPath LIS</span>
                <span className="text-[10px] uppercase font-bold px-2 py-0.5 rounded bg-sky-950 text-sky-400 border border-sky-800">
                  ISO 15189 Certified
                </span>
              </div>
              <p className="text-xs text-slate-400 hidden sm:block">Clinical Laboratory Information & Diagnostic Management</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            {/* Instant Demo Role Switcher */}
            <div className="flex items-center gap-1 bg-slate-800 p-1 rounded-lg border border-slate-700 text-xs">
              <span className="text-slate-400 px-2 font-medium hidden md:inline">Role:</span>
              {(['ADMIN', 'RECEPTIONIST', 'TECHNICIAN', 'DOCTOR', 'PATIENT'] as RoleType[]).map((r) => (
                <button
                  key={r}
                  onClick={() => switchRoleDemo(r)}
                  className={`px-2 py-1 rounded text-xs font-semibold transition-all ${
                    user?.role === r
                      ? 'bg-sky-600 text-white shadow-sm'
                      : 'text-slate-400 hover:text-white hover:bg-slate-700'
                  }`}
                >
                  {r.slice(0, 4)}
                </button>
              ))}
            </div>

            <button
              onClick={() => setShowQrModal(true)}
              className="p-2 bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-lg text-slate-300 hover:text-white"
              title="Verify Report QR"
            >
              <QrCode className="w-4 h-4" />
            </button>

            <button
              onClick={logout}
              className="p-2 bg-rose-500/20 hover:bg-rose-500/30 text-rose-300 border border-rose-500/30 rounded-lg"
              title="Sign Out"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Clinical Lifecycle Tabs */}
        <div className="max-w-7xl mx-auto px-4 flex gap-1 overflow-x-auto border-t border-slate-800 text-xs font-medium">
          {[
            { id: 'reception', label: '1. Reception & Booking', icon: Users, roles: ['ADMIN', 'RECEPTIONIST', 'DOCTOR'] },
            { id: 'phlebotomy', label: '2. Phlebotomy & Samples', icon: Droplets, roles: ['ADMIN', 'RECEPTIONIST', 'TECHNICIAN'] },
            { id: 'lab-worklist', label: '3. Lab Worklist & Results', icon: Activity, roles: ['ADMIN', 'TECHNICIAN', 'DOCTOR'] },
            { id: 'verifications', label: '4. Doctor Sign-off', icon: ClipboardCheck, roles: ['ADMIN', 'DOCTOR'] },
            { id: 'reports', label: '5. Reports & Delivery', icon: FileText, roles: ['ADMIN', 'RECEPTIONIST', 'TECHNICIAN', 'DOCTOR', 'PATIENT'] },
            { id: 'analytics', label: '6. Analytics & Financials', icon: BarChart3, roles: ['ADMIN', 'DOCTOR'] },
            { id: 'audit', label: '7. ISO Audit Trail', icon: ShieldCheck, roles: ['ADMIN'] },
          ]
            .filter((tab) => hasRole(tab.roles as RoleType[]))
            .map((tab) => {
              const Icon = tab.icon;
              const active = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2 py-3 px-3 border-b-2 font-semibold transition-colors whitespace-nowrap ${
                    active
                      ? 'border-sky-500 text-sky-400 bg-slate-800/40'
                      : 'border-transparent text-slate-400 hover:text-slate-200'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
        </div>
      </header>

      {/* Notification Toast */}
      {notification && (
        <div
          className={`fixed bottom-6 right-6 z-50 px-4 py-3 rounded-xl shadow-2xl text-sm font-medium flex items-center gap-2 border animate-in slide-in-from-bottom ${
            notification.type === 'success'
              ? 'bg-emerald-900 text-emerald-100 border-emerald-700'
              : 'bg-rose-900 text-rose-100 border-rose-700'
          }`}
        >
          {notification.type === 'success' ? <CheckCircle2 className="w-5 h-5 text-emerald-400" /> : <AlertTriangle className="w-5 h-5 text-rose-400" />}
          <span>{notification.message}</span>
        </div>
      )}

      {/* Main Content Area */}
      <main className="max-w-7xl w-full mx-auto p-4 sm:p-6 flex-1">
        {/* KPI Mini-Cards Banner */}
        {kpis && (
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 mb-6">
            <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
              <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Total Patients</div>
              <div className="text-xl font-bold text-slate-800 mt-1">{kpis.total_patients}</div>
            </div>
            <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
              <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Total Orders</div>
              <div className="text-xl font-bold text-slate-800 mt-1">{kpis.total_orders}</div>
            </div>
            <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
              <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Gross Revenue</div>
              <div className="text-xl font-bold text-emerald-600 mt-1">${kpis.total_revenue.toFixed(2)}</div>
            </div>
            <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
              <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">In-Lab Samples</div>
              <div className="text-xl font-bold text-sky-600 mt-1">{kpis.samples_in_lab}</div>
            </div>
            <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
              <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Completed</div>
              <div className="text-xl font-bold text-indigo-600 mt-1">{kpis.completed_orders}</div>
            </div>
            <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
              <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Avg TAT</div>
              <div className="text-xl font-bold text-amber-600 mt-1">{kpis.avg_turnaround_time_hours} hrs</div>
            </div>
          </div>
        )}

        {/* TAB 1: RECEPTION & ORDER BOOKING */}
        {activeTab === 'reception' && (
          <div className="space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <h2 className="text-lg font-bold text-slate-900">Patient Registration & Order Management</h2>
                <p className="text-xs text-slate-500">Register new clinical patients, place diagnostic orders, and process payments</p>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => setShowNewPatientModal(true)}
                  className="px-3.5 py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-lg text-xs font-semibold flex items-center gap-1.5 shadow-sm"
                >
                  <Plus className="w-4 h-4" /> Register Patient
                </button>
                <button
                  onClick={() => setShowNewOrderModal(true)}
                  className="px-3.5 py-2 bg-sky-600 hover:bg-sky-500 text-white rounded-lg text-xs font-semibold flex items-center gap-1.5 shadow-sm shadow-sky-600/20"
                >
                  <FileSpreadsheet className="w-4 h-4" /> Place Test Order
                </button>
              </div>
            </div>

            {/* Orders Data Table */}
            <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
              <div className="p-4 border-b border-slate-200 flex items-center justify-between gap-4">
                <div className="relative flex-1 max-w-md">
                  <Search className="w-4 h-4 absolute left-3 top-2.5 text-slate-400" />
                  <input
                    type="text"
                    placeholder="Search by order number or patient name..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full pl-9 pr-3 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:border-sky-500"
                  />
                </div>
                <button onClick={refreshData} className="p-1.5 text-slate-500 hover:text-slate-800 rounded-lg hover:bg-slate-100">
                  <RefreshCw className="w-4 h-4" />
                </button>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-50 text-slate-600 uppercase font-semibold border-b border-slate-200">
                    <tr>
                      <th className="px-4 py-3">Order #</th>
                      <th className="px-4 py-3">Patient</th>
                      <th className="px-4 py-3">Ordered Tests</th>
                      <th className="px-4 py-3">Priority</th>
                      <th className="px-4 py-3">Total / Paid</th>
                      <th className="px-4 py-3">Status</th>
                      <th className="px-4 py-3 text-right">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {orders
                      .filter((o) =>
                        o.order_number.toLowerCase().includes(searchQuery.toLowerCase()) ||
                        (o.patient?.full_name || '').toLowerCase().includes(searchQuery.toLowerCase())
                      )
                      .map((o) => (
                        <tr key={o.id} className="hover:bg-slate-50/80 transition-colors">
                          <td className="px-4 py-3 font-bold text-slate-900">{o.order_number}</td>
                          <td className="px-4 py-3">
                            <div className="font-semibold text-slate-800">{o.patient?.first_name} {o.patient?.last_name}</div>
                            <div className="text-[10px] text-slate-400">{o.patient?.patient_code} &bull; {o.patient?.gender}</div>
                          </td>
                          <td className="px-4 py-3">
                            <div className="flex flex-wrap gap-1">
                              {o.order_items.map((it) => (
                                <span key={it.id} className="px-1.5 py-0.5 bg-slate-100 border border-slate-200 text-[10px] rounded font-medium text-slate-700">
                                  {it.test?.test_code || 'Test'}
                                </span>
                              ))}
                            </div>
                          </td>
                          <td className="px-4 py-3">
                            <span
                              className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                                o.priority === 'STAT'
                                  ? 'bg-rose-100 text-rose-700 border border-rose-200 animate-pulse'
                                  : o.priority === 'URGENT'
                                  ? 'bg-amber-100 text-amber-700 border border-amber-200'
                                  : 'bg-slate-100 text-slate-600'
                              }`}
                            >
                              {o.priority}
                            </span>
                          </td>
                          <td className="px-4 py-3">
                            <div className="font-semibold text-slate-800">${o.total_amount.toFixed(2)}</div>
                            <div className="text-[10px] text-emerald-600">Paid: ${(o.invoice?.paid_amount || 0).toFixed(2)}</div>
                          </td>
                          <td className="px-4 py-3">
                            <span
                              className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                                o.status === 'COMPLETED'
                                  ? 'bg-emerald-100 text-emerald-800'
                                  : o.status === 'IN_PROGRESS' || o.status === 'SAMPLE_COLLECTED'
                                  ? 'bg-sky-100 text-sky-800'
                                  : 'bg-slate-100 text-slate-600'
                              }`}
                            >
                              {o.status}
                            </span>
                          </td>
                          <td className="px-4 py-3 text-right">
                            {o.invoice && o.invoice.balance_amount > 0 && (
                              <button
                                onClick={async () => {
                                  const amt = prompt(`Enter payment amount (Balance: $${o.invoice?.balance_amount}):`, String(o.invoice?.balance_amount));
                                  if (amt) {
                                    await apiClient.post(`/orders/${o.id}/payments`, { amount: Number(amt), payment_method: 'CASH' });
                                    showToast('Payment recorded');
                                    refreshData();
                                  }
                                }}
                                className="px-2 py-1 bg-emerald-600 hover:bg-emerald-500 text-white rounded text-[10px] font-semibold"
                              >
                                Pay
                              </button>
                            )}
                          </td>
                        </tr>
                      ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* TAB 2: PHLEBOTOMY & SAMPLES */}
        {activeTab === 'phlebotomy' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-lg font-bold text-slate-900">Phlebotomy Workstation & Sample Accessioning</h2>
                <p className="text-xs text-slate-500">Collect specimens, print barcodes, and accession tubes into the lab</p>
              </div>
              <button onClick={refreshData} className="p-2 text-slate-500 hover:text-slate-800 rounded-lg hover:bg-slate-200">
                <RefreshCw className="w-4 h-4" />
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {samples.map((s) => {
                const isCollected = s.status === 'COLLECTED';
                const isPending = s.status === 'PENDING_COLLECTION';
                const isInLab = s.status === 'RECEIVED_IN_LAB' || s.status === 'PROCESSING';
                const isRejected = s.status === 'REJECTED';

                return (
                  <div key={s.id} className="bg-white rounded-xl border border-slate-200 shadow-sm p-4 flex flex-col justify-between">
                    <div>
                      <div className="flex items-start justify-between gap-2 mb-2">
                        <div className="font-mono font-bold text-sm bg-slate-900 text-sky-400 px-2.5 py-1 rounded">
                          {s.barcode}
                        </div>
                        <span
                          className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                            isRejected
                              ? 'bg-rose-100 text-rose-700'
                              : isInLab
                              ? 'bg-indigo-100 text-indigo-700'
                              : isCollected
                              ? 'bg-emerald-100 text-emerald-700'
                              : 'bg-amber-100 text-amber-700'
                          }`}
                        >
                          {s.status}
                        </span>
                      </div>

                      <div className="text-xs font-semibold text-slate-800">{s.specimen_type}</div>
                      <div className="text-[11px] text-slate-500 mt-0.5">Container: <span className="font-medium text-slate-700">{s.container_type}</span></div>
                      {s.notes && <div className="text-[11px] text-slate-600 mt-2 p-2 bg-slate-50 rounded border border-slate-100">{s.notes}</div>}
                    </div>

                    <div className="mt-4 pt-3 border-t border-slate-100 flex gap-2">
                      {isPending && (
                        <button
                          onClick={() => handleSampleAction(s.id, 'collect')}
                          className="flex-1 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-semibold flex items-center justify-center gap-1"
                        >
                          <Check className="w-3.5 h-3.5" /> Mark Collected
                        </button>
                      )}
                      {isCollected && (
                        <button
                          onClick={() => handleSampleAction(s.id, 'receive')}
                          className="flex-1 py-1.5 bg-sky-600 hover:bg-sky-500 text-white rounded-lg text-xs font-semibold flex items-center justify-center gap-1"
                        >
                          <FlaskConical className="w-3.5 h-3.5" /> Accession in Lab
                        </button>
                      )}
                      {!isRejected && (
                        <button
                          onClick={() => {
                            const reason = prompt('Enter clinical rejection reason (e.g. Hemolyzed, Clotted, Insufficient):');
                            if (reason) handleSampleAction(s.id, 'reject', reason);
                          }}
                          className="px-2 py-1.5 bg-rose-50 hover:bg-rose-100 text-rose-600 border border-rose-200 rounded-lg text-xs font-semibold"
                        >
                          Reject
                        </button>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* TAB 3: TECHNICIAN WORKLIST & RESULTS */}
        {activeTab === 'lab-worklist' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-lg font-bold text-slate-900">Laboratory Technician Testing Worklist</h2>
                <p className="text-xs text-slate-500">Record parameter results with automated reference bounds and abnormal flagging</p>
              </div>
              <button onClick={refreshData} className="p-2 text-slate-500 hover:text-slate-800 rounded-lg hover:bg-slate-200">
                <RefreshCw className="w-4 h-4" />
              </button>
            </div>

            <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-50 text-slate-600 uppercase font-semibold border-b border-slate-200">
                    <tr>
                      <th className="px-4 py-3">Order / Priority</th>
                      <th className="px-4 py-3">Patient</th>
                      <th className="px-4 py-3">Investigation</th>
                      <th className="px-4 py-3">Tube Barcode</th>
                      <th className="px-4 py-3">Status</th>
                      <th className="px-4 py-3 text-right">Result Entry</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {worklist.map((item) => (
                      <tr key={item.order_item_id} className="hover:bg-slate-50 transition-colors">
                        <td className="px-4 py-3">
                          <div className="font-bold text-slate-900">{item.order_number}</div>
                          <span
                            className={`px-1.5 py-0.5 rounded text-[9px] font-extrabold uppercase ${
                              item.priority === 'STAT'
                                ? 'bg-rose-600 text-white animate-pulse'
                                : item.priority === 'URGENT'
                                ? 'bg-amber-500 text-white'
                                : 'bg-slate-200 text-slate-700'
                            }`}
                          >
                            {item.priority}
                          </span>
                        </td>
                        <td className="px-4 py-3">
                          <div className="font-semibold text-slate-800">{item.patient_name}</div>
                          <div className="text-[10px] text-slate-400">{item.patient_gender}, {item.patient_age} yrs</div>
                        </td>
                        <td className="px-4 py-3 font-semibold text-slate-800">
                          {item.test_name} ({item.test_code})
                        </td>
                        <td className="px-4 py-3 font-mono font-bold text-slate-700">
                          {item.sample_barcode}
                        </td>
                        <td className="px-4 py-3">
                          <span className="px-2 py-0.5 bg-sky-100 text-sky-800 rounded font-semibold text-[10px]">
                            {item.item_status} ({item.results_count}/{item.parameters_count})
                          </span>
                        </td>
                        <td className="px-4 py-3 text-right">
                          <button
                            onClick={async () => {
                              // Fetch parameters for this test
                              const testRes = await apiClient.get(`/catalog/tests/${item.test_id}`);
                              setShowResultEntryModal({ ...item, testDetails: testRes.data });
                              // Prefill existing results
                              const resRes = await apiClient.get(`/results/order/${item.order_id}`);
                              const inputMap: any = {};
                              resRes.data.forEach((r: any) => {
                                inputMap[r.parameter_id] = {
                                  numeric_value: r.numeric_value,
                                  text_value: r.text_value,
                                  notes: r.technician_notes,
                                };
                              });
                              setResultInputs(inputMap);
                            }}
                            className="px-3 py-1.5 bg-sky-600 hover:bg-sky-500 text-white rounded-lg text-xs font-semibold shadow-sm"
                          >
                            Enter Results
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* TAB 4: DOCTOR SIGN-OFF */}
        {activeTab === 'verifications' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-lg font-bold text-slate-900">Pathologist Verification & Medical Sign-off</h2>
                <p className="text-xs text-slate-500">Review completed lab results, abnormal alerts, and sign off official reports</p>
              </div>
              <button onClick={refreshData} className="p-2 text-slate-500 hover:text-slate-800 rounded-lg hover:bg-slate-200">
                <RefreshCw className="w-4 h-4" />
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {reports.map((rep) => (
                <div key={rep.id} className="bg-white rounded-xl border border-slate-200 shadow-sm p-4 flex flex-col justify-between">
                  <div>
                    <div className="flex items-center justify-between mb-3">
                      <div className="font-bold text-sm text-slate-900">{rep.report_number}</div>
                      <span
                        className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                          rep.status === 'VERIFIED' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'
                        }`}
                      >
                        {rep.status}
                      </span>
                    </div>
                    <div className="text-xs text-slate-600 space-y-1">
                      <div>Order ID: <span className="font-mono font-medium text-slate-800">{rep.order_id.slice(0, 8)}...</span></div>
                      <div>Created: <span className="font-medium text-slate-800">{new Date(rep.created_at).toLocaleString()}</span></div>
                      {rep.verified_at && (
                        <div>Verified: <span className="font-medium text-emerald-700">{new Date(rep.verified_at).toLocaleString()}</span></div>
                      )}
                    </div>
                  </div>

                  <div className="mt-4 pt-3 border-t border-slate-100 flex gap-2">
                    {rep.status === 'DRAFT' && (
                      <button
                        onClick={() => setShowVerifyModal(rep)}
                        className="flex-1 py-2 bg-sky-600 hover:bg-sky-500 text-white rounded-lg text-xs font-semibold flex items-center justify-center gap-1 shadow-sm"
                      >
                        <ClipboardCheck className="w-4 h-4" /> Review & Sign Off
                      </button>
                    )}
                    {rep.status === 'VERIFIED' && (
                      <a
                        href={`http://localhost:8000/api/v1/reports/${rep.id}/pdf?token=${token || ''}`}
                        target="_blank"
                        rel="noreferrer"
                        className="flex-1 py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-lg text-xs font-semibold flex items-center justify-center gap-1 shadow-sm text-center"
                      >
                        <Download className="w-4 h-4" /> Download PDF Report
                      </a>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 5: REPORTS & DELIVERY */}
        {activeTab === 'reports' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-lg font-bold text-slate-900">Diagnostic Reports Library</h2>
                <p className="text-xs text-slate-500">Access and download verified patient laboratory test reports</p>
              </div>
            </div>

            <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-50 text-slate-600 uppercase font-semibold border-b border-slate-200">
                  <tr>
                    <th className="px-4 py-3">Report #</th>
                    <th className="px-4 py-3">Status</th>
                    <th className="px-4 py-3">Verified By</th>
                    <th className="px-4 py-3">Verification Hash</th>
                    <th className="px-4 py-3 text-right">PDF</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {reports.map((rep) => (
                    <tr key={rep.id} className="hover:bg-slate-50 transition-colors">
                      <td className="px-4 py-3 font-bold text-slate-900">{rep.report_number}</td>
                      <td className="px-4 py-3">
                        <span
                          className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                            rep.status === 'VERIFIED' ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-100 text-slate-600'
                          }`}
                        >
                          {rep.status}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-slate-700">
                        {rep.verified_by_doctor ? `Dr. ${rep.verified_by_doctor.first_name} ${rep.verified_by_doctor.last_name}` : 'Pending'}
                      </td>
                      <td className="px-4 py-3 font-mono text-[10px] text-slate-500">
                        {rep.verification_qr_hash.slice(0, 16)}...
                      </td>
                      <td className="px-4 py-3 text-right">
                        <a
                          href={`http://localhost:8000/api/v1/reports/${rep.id}/pdf?token=${token || ''}`}
                          target="_blank"
                          rel="noreferrer"
                          className="px-3 py-1.5 bg-slate-900 hover:bg-slate-800 text-white rounded text-xs font-semibold inline-flex items-center gap-1"
                        >
                          <Download className="w-3.5 h-3.5" /> PDF
                        </a>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* TAB 6: ANALYTICS & FINANCIALS */}
        {activeTab === 'analytics' && (
          <div className="space-y-6">
            <div>
              <h2 className="text-lg font-bold text-slate-900">Laboratory Operations & Financial Intelligence</h2>
              <p className="text-xs text-slate-500">Time-series revenue trends, most requested panels, and turnaround metrics</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Daily Revenue Trend Cards */}
              <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-4">
                <h3 className="text-sm font-bold text-slate-900 mb-3 flex items-center gap-2">
                  <DollarSign className="w-4 h-4 text-emerald-600" /> Recent Daily Revenue Performance
                </h3>
                <div className="space-y-2">
                  {revenueTrends.map((t, idx) => (
                    <div key={idx} className="flex items-center justify-between p-2.5 bg-slate-50 rounded-lg text-xs">
                      <span className="font-semibold text-slate-700">{t.period}</span>
                      <div className="text-right">
                        <div className="font-bold text-emerald-600">${t.gross_revenue.toFixed(2)}</div>
                        <div className="text-[10px] text-slate-400">{t.order_count} orders</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Most Requested Tests */}
              <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-4">
                <h3 className="text-sm font-bold text-slate-900 mb-3 flex items-center gap-2">
                  <Activity className="w-4 h-4 text-sky-600" /> Most Requested Clinical Tests
                </h3>
                <div className="space-y-2">
                  {mostRequested.map((t) => (
                    <div key={t.test_id} className="flex items-center justify-between p-2.5 bg-slate-50 rounded-lg text-xs">
                      <div>
                        <div className="font-semibold text-slate-800">{t.test_name} ({t.test_code})</div>
                        <div className="text-[10px] text-slate-400">{t.category_name}</div>
                      </div>
                      <div className="text-right">
                        <div className="font-bold text-slate-900">{t.order_count} orders</div>
                        <div className="text-[10px] text-emerald-600">${t.total_revenue_generated.toFixed(2)}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* TAB 7: AUDIT LOGS */}
        {activeTab === 'audit' && (
          <div className="space-y-6">
            <div>
              <h2 className="text-lg font-bold text-slate-900">ISO 15189 / HIPAA Regulatory Audit Trail</h2>
              <p className="text-xs text-slate-500">Immutable change log capturing all diagnostic events, actors, and timestamps</p>
            </div>

            <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-50 text-slate-600 uppercase font-semibold border-b border-slate-200">
                  <tr>
                    <th className="px-4 py-3">Timestamp</th>
                    <th className="px-4 py-3">Action</th>
                    <th className="px-4 py-3">Entity</th>
                    <th className="px-4 py-3">Event Details</th>
                    <th className="px-4 py-3">IP Address</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {auditLogs.map((log) => (
                    <tr key={log.id} className="hover:bg-slate-50 transition-colors">
                      <td className="px-4 py-3 text-slate-500 whitespace-nowrap">
                        {new Date(log.timestamp).toLocaleString()}
                      </td>
                      <td className="px-4 py-3">
                        <span className="px-2 py-0.5 bg-slate-100 text-slate-800 rounded font-mono font-bold text-[10px]">
                          {log.action}
                        </span>
                      </td>
                      <td className="px-4 py-3 font-semibold text-slate-700">{log.entity_name}</td>
                      <td className="px-4 py-3 text-slate-800">{log.details}</td>
                      <td className="px-4 py-3 font-mono text-[10px] text-slate-400">{log.ip_address || '127.0.0.1'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </main>

      {/* MODAL 1: REGISTER PATIENT */}
      {showNewPatientModal && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl border border-slate-200">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-base font-bold text-slate-900">Register New Patient</h3>
              <button onClick={() => setShowNewPatientModal(false)} className="text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>
            <form onSubmit={handleCreatePatient} className="space-y-3 text-xs">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">First Name</label>
                  <input
                    type="text"
                    required
                    value={patientForm.first_name}
                    onChange={(e) => setPatientForm({ ...patientForm, first_name: e.target.value })}
                    className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2 focus:outline-none focus:border-sky-500"
                  />
                </div>
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Last Name</label>
                  <input
                    type="text"
                    required
                    value={patientForm.last_name}
                    onChange={(e) => setPatientForm({ ...patientForm, last_name: e.target.value })}
                    className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2 focus:outline-none focus:border-sky-500"
                  />
                </div>
              </div>
              <div className="grid grid-cols-3 gap-3">
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">DOB</label>
                  <input
                    type="date"
                    required
                    value={patientForm.date_of_birth}
                    onChange={(e) => setPatientForm({ ...patientForm, date_of_birth: e.target.value })}
                    className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2 focus:outline-none focus:border-sky-500"
                  />
                </div>
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Gender</label>
                  <select
                    value={patientForm.gender}
                    onChange={(e) => setPatientForm({ ...patientForm, gender: e.target.value as any })}
                    className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2 focus:outline-none focus:border-sky-500"
                  >
                    <option value="MALE">Male</option>
                    <option value="FEMALE">Female</option>
                    <option value="OTHER">Other</option>
                  </select>
                </div>
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Blood Group</label>
                  <select
                    value={patientForm.blood_group}
                    onChange={(e) => setPatientForm({ ...patientForm, blood_group: e.target.value })}
                    className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2 focus:outline-none focus:border-sky-500"
                  >
                    <option value="O+">O+</option>
                    <option value="O-">O-</option>
                    <option value="A+">A+</option>
                    <option value="A-">A-</option>
                    <option value="B+">B+</option>
                    <option value="B-">B-</option>
                    <option value="AB+">AB+</option>
                    <option value="AB-">AB-</option>
                  </select>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Phone</label>
                  <input
                    type="tel"
                    required
                    value={patientForm.phone}
                    onChange={(e) => setPatientForm({ ...patientForm, phone: e.target.value })}
                    className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2 focus:outline-none focus:border-sky-500"
                  />
                </div>
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Email</label>
                  <input
                    type="email"
                    value={patientForm.email}
                    onChange={(e) => setPatientForm({ ...patientForm, email: e.target.value })}
                    className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2 focus:outline-none focus:border-sky-500"
                  />
                </div>
              </div>
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Medical Notes</label>
                <textarea
                  rows={2}
                  value={patientForm.medical_history_notes}
                  onChange={(e) => setPatientForm({ ...patientForm, medical_history_notes: e.target.value })}
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2 focus:outline-none focus:border-sky-500"
                  placeholder="Known allergies, existing conditions, or medications..."
                />
              </div>
              <div className="pt-3 flex gap-2 justify-end">
                <button
                  type="button"
                  onClick={() => setShowNewPatientModal(false)}
                  className="px-4 py-2 border border-slate-200 text-slate-600 rounded-lg font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-sky-600 hover:bg-sky-500 text-white rounded-lg font-semibold shadow-sm"
                >
                  Register Patient
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* MODAL 2: PLACE TEST ORDER */}
      {showNewOrderModal && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-xl w-full p-6 shadow-2xl border border-slate-200">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-base font-bold text-slate-900">Place Clinical Laboratory Order</h3>
              <button onClick={() => setShowNewOrderModal(false)} className="text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>
            <form onSubmit={handleCreateOrder} className="space-y-4 text-xs">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Select Patient</label>
                <select
                  required
                  value={orderForm.patient_id}
                  onChange={(e) => setOrderForm({ ...orderForm, patient_id: e.target.value })}
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2 focus:outline-none focus:border-sky-500"
                >
                  <option value="">-- Choose Registered Patient --</option>
                  {patients.map((p) => (
                    <option key={p.id} value={p.id}>
                      {p.first_name} {p.last_name} ({p.patient_code}) - {p.phone}
                    </option>
                  ))}
                </select>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Referring Doctor</label>
                  <input
                    type="text"
                    placeholder="e.g. Dr. Robert Vance"
                    value={orderForm.referring_doctor}
                    onChange={(e) => setOrderForm({ ...orderForm, referring_doctor: e.target.value })}
                    className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2 focus:outline-none focus:border-sky-500"
                  />
                </div>
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Priority</label>
                  <select
                    value={orderForm.priority}
                    onChange={(e) => setOrderForm({ ...orderForm, priority: e.target.value as any })}
                    className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2 focus:outline-none focus:border-sky-500 font-bold"
                  >
                    <option value="ROUTINE">ROUTINE</option>
                    <option value="URGENT">URGENT</option>
                    <option value="STAT">STAT (Critical Immediate)</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Select Test Panels & Investigations</label>
                <div className="max-h-48 overflow-y-auto border border-slate-200 rounded-lg p-2 space-y-1 bg-slate-50">
                  {catalog.map((t) => {
                    const isChecked = orderForm.selected_test_ids.includes(t.id);
                    return (
                      <label key={t.id} className="flex items-center justify-between p-2 rounded hover:bg-slate-100 cursor-pointer">
                        <div className="flex items-center gap-2">
                          <input
                            type="checkbox"
                            checked={isChecked}
                            onChange={(e) => {
                              if (e.target.checked) {
                                setOrderForm({ ...orderForm, selected_test_ids: [...orderForm.selected_test_ids, t.id] });
                              } else {
                                setOrderForm({
                                  ...orderForm,
                                  selected_test_ids: orderForm.selected_test_ids.filter((id) => id !== t.id),
                                });
                              }
                            }}
                            className="rounded text-sky-600 focus:ring-sky-500"
                          />
                          <div>
                            <span className="font-semibold text-slate-800">{t.name}</span>
                            <span className="text-[10px] text-slate-400 ml-1.5 font-mono">({t.test_code}) &bull; {t.container_type}</span>
                          </div>
                        </div>
                        <span className="font-bold text-emerald-600">${t.price.toFixed(2)}</span>
                      </label>
                    );
                  })}
                </div>
              </div>

              <div className="p-3 bg-sky-50 rounded-lg border border-sky-100 flex items-center justify-between">
                <span className="font-semibold text-sky-900">Total Order Amount:</span>
                <span className="text-base font-bold text-sky-900">
                  ${catalog
                    .filter((t) => orderForm.selected_test_ids.includes(t.id))
                    .reduce((sum, t) => sum + t.price, 0)
                    .toFixed(2)}
                </span>
              </div>

              <div className="pt-2 flex gap-2 justify-end">
                <button
                  type="button"
                  onClick={() => setShowNewOrderModal(false)}
                  className="px-4 py-2 border border-slate-200 text-slate-600 rounded-lg font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-sky-600 hover:bg-sky-500 text-white rounded-lg font-semibold shadow-sm"
                >
                  Book Order & Generate Barcodes
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* MODAL 3: BATCH RESULT ENTRY */}
      {showResultEntryModal && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-2xl w-full p-6 shadow-2xl border border-slate-200 max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-4 border-b pb-3">
              <div>
                <h3 className="text-base font-bold text-slate-900">
                  {showResultEntryModal.test_name} ({showResultEntryModal.test_code})
                </h3>
                <p className="text-xs text-slate-500">
                  Patient: <span className="font-semibold">{showResultEntryModal.patient_name}</span> ({showResultEntryModal.patient_gender}, {showResultEntryModal.patient_age} yrs) &bull; Tube: <span className="font-mono">{showResultEntryModal.sample_barcode}</span>
                </p>
              </div>
              <button onClick={() => setShowResultEntryModal(null)} className="text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleBatchResultsSubmit} className="space-y-4 text-xs">
              <table className="w-full text-left">
                <thead className="bg-slate-50 text-slate-600 font-semibold border-b">
                  <tr>
                    <th className="p-2">Parameter</th>
                    <th className="p-2">Observed Value</th>
                    <th className="p-2">Unit</th>
                    <th className="p-2">Biological Reference Interval</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {showResultEntryModal.testDetails?.parameters?.map((p: any) => {
                    const current = resultInputs[p.id] || {};
                    const normalRange = p.reference_ranges?.[0];
                    const rangeDisplay = normalRange
                      ? `${normalRange.normal_min || ''} - ${normalRange.normal_max || ''}`
                      : 'Standard';

                    return (
                      <tr key={p.id}>
                        <td className="p-2 font-semibold text-slate-800">{p.name}</td>
                        <td className="p-2">
                          {p.data_type === 'NUMERIC' ? (
                            <input
                              type="number"
                              step="any"
                              required
                              placeholder="Value"
                              value={current.numeric_value ?? ''}
                              onChange={(e) =>
                                setResultInputs({
                                  ...resultInputs,
                                  [p.id]: { ...current, numeric_value: e.target.value ? parseFloat(e.target.value) : undefined },
                                })
                              }
                              className="w-28 bg-slate-50 border border-slate-200 rounded p-1.5 text-xs font-bold text-slate-900 focus:outline-none focus:border-sky-500"
                            />
                          ) : (
                            <input
                              type="text"
                              required
                              placeholder="Observation"
                              value={current.text_value ?? ''}
                              onChange={(e) =>
                                setResultInputs({
                                  ...resultInputs,
                                  [p.id]: { ...current, text_value: e.target.value },
                                })
                              }
                              className="w-36 bg-slate-50 border border-slate-200 rounded p-1.5 text-xs font-bold text-slate-900 focus:outline-none focus:border-sky-500"
                            />
                          )}
                        </td>
                        <td className="p-2 text-slate-500">{p.unit || '-'}</td>
                        <td className="p-2 text-slate-600 font-mono text-[11px]">{rangeDisplay}</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>

              <div className="pt-4 flex gap-2 justify-end border-t">
                <button
                  type="button"
                  onClick={() => setShowResultEntryModal(null)}
                  className="px-4 py-2 border border-slate-200 text-slate-600 rounded-lg font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-sky-600 hover:bg-sky-500 text-white rounded-lg font-semibold shadow-sm"
                >
                  Save Results & Evaluate Flags
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* MODAL 4: DOCTOR VERIFICATION */}
      {showVerifyModal && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl border border-slate-200">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-base font-bold text-slate-900">Doctor Verification & Sign-off</h3>
              <button onClick={() => setShowVerifyModal(null)} className="text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>
            <div className="space-y-4 text-xs">
              <p className="text-slate-600">
                You are about to digitally verify and stamp laboratory report <strong className="text-slate-900">{showVerifyModal.report_number}</strong>. This will compile the permanent official PDF.
              </p>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Pathologist Comments</label>
                <textarea
                  rows={2}
                  value={verifyComments}
                  onChange={(e) => setVerifyComments(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2 focus:outline-none focus:border-sky-500"
                  placeholder="Clinical remarks regarding observed parameters..."
                />
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Clinical Interpretation</label>
                <textarea
                  rows={2}
                  value={verifyInterpretation}
                  onChange={(e) => setVerifyInterpretation(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2 focus:outline-none focus:border-sky-500"
                  placeholder="Diagnostic impression and follow-up guidance..."
                />
              </div>

              <div className="pt-2 flex gap-2 justify-end">
                <button
                  type="button"
                  onClick={() => setShowVerifyModal(null)}
                  className="px-4 py-2 border border-slate-200 text-slate-600 rounded-lg font-semibold"
                >
                  Cancel
                </button>
                <button
                  onClick={handleVerifyReport}
                  className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg font-semibold shadow-sm"
                >
                  Digitally Sign & Publish Report
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* MODAL 5: QR VERIFICATION */}
      {showQrModal && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl border border-slate-200">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                <QrCode className="w-5 h-5 text-sky-600" /> Tamper-Proof QR Verification
              </h3>
              <button onClick={() => { setShowQrModal(false); setQrVerifyResult(null); }} className="text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>
            <div className="space-y-4 text-xs">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Report QR Hash Token</label>
                <input
                  type="text"
                  placeholder="Paste verification token or hash..."
                  value={qrVerifyHash}
                  onChange={(e) => setQrVerifyHash(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2 font-mono text-xs focus:outline-none focus:border-sky-500"
                />
              </div>
              <button
                onClick={handleVerifyQr}
                className="w-full py-2 bg-slate-900 hover:bg-slate-800 text-white font-semibold rounded-lg"
              >
                Verify Authenticity in Central Registry
              </button>

              {qrVerifyResult && (
                <div className={`p-3 rounded-lg border text-xs ${qrVerifyResult.is_authentic ? 'bg-emerald-50 border-emerald-200 text-emerald-900' : 'bg-rose-50 border-rose-200 text-rose-900'}`}>
                  {qrVerifyResult.is_authentic ? (
                    <div className="space-y-1">
                      <div className="font-bold flex items-center gap-1.5 text-emerald-700">
                        <CheckCircle2 className="w-4 h-4" /> Authenticated Original Medical Record
                      </div>
                      <div>Report: <span className="font-semibold">{qrVerifyResult.report_number}</span></div>
                      <div>Patient Initials: <span className="font-semibold">{qrVerifyResult.patient_initials}</span> ({qrVerifyResult.patient_code})</div>
                      <div>Verified By: <span className="font-semibold">{qrVerifyResult.verified_by}</span></div>
                      <div>Lab: <span className="font-semibold">{qrVerifyResult.laboratory_name}</span></div>
                    </div>
                  ) : (
                    <div className="font-bold flex items-center gap-1.5 text-rose-700">
                      <AlertTriangle className="w-4 h-4" /> {qrVerifyResult.error}
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
