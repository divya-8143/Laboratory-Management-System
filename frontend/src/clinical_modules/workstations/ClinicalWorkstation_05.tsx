import React from 'react';

export interface WorkstationProps_5 {
  workstationId: string;
  department: string;
  activeOperator: string;
  onRefresh?: () => void;
}

export const ClinicalWorkstation_5: React.FC<WorkstationProps_5> = (props) => {
  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6 space-y-4">
      <div className="flex items-center justify-between border-b border-slate-100 pb-3">
        <div>
          <h3 className="text-base font-bold text-slate-900">Clinical Workstation Matrix 5</h3>
          <p className="text-xs text-slate-500">Department: {props.department} | Operator: {props.activeOperator}</p>
        </div>
        <span className="px-2.5 py-1 bg-emerald-50 text-emerald-700 rounded-full text-xs font-semibold">
          SYSTEM ACTIVE
        </span>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        <div className="bg-slate-50 p-3 rounded-lg border border-slate-200">
          <div className="text-[11px] font-semibold text-slate-500 uppercase">Assay Queue</div>
          <div className="text-lg font-bold text-slate-800 mt-1">128 Pending</div>
        </div>
        <div className="bg-slate-50 p-3 rounded-lg border border-slate-200">
          <div className="text-[11px] font-semibold text-slate-500 uppercase">QC Status</div>
          <div className="text-lg font-bold text-emerald-600 mt-1">Westgard Valid</div>
        </div>
        <div className="bg-slate-50 p-3 rounded-lg border border-slate-200">
          <div className="text-[11px] font-semibold text-slate-500 uppercase">Throughput</div>
          <div className="text-lg font-bold text-sky-600 mt-1">450 tests/hr</div>
        </div>
      </div>
    </div>
  );
};
