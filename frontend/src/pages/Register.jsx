import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { ArrowRight, Eye, EyeOff, Lock, Mail, User } from "lucide-react";

import { api } from "../api";

export default function Register() {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [messageTone, setMessageTone] = useState("error");
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const register = async () => {
    const normalizedName = name.trim();
    const normalizedEmail = email.trim().toLowerCase();
    if (!normalizedName) return setMessage("Please enter your full name.");
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(normalizedEmail)) return setMessage("Please enter a valid email address.");
    if (password.length < 6) return setMessage("Password must be at least 6 characters.");
    try {
      setLoading(true);
      await api.post("/auth/register", { name: normalizedName, email: normalizedEmail, password });
      setMessageTone("success");
      setMessage("Account created. Redirecting to sign in...");
      setTimeout(() => navigate("/login"), 900);
    } catch (e) {
      setMessageTone("error");
      setMessage(e.response?.data?.error || "Unable to create account.");
      setLoading(false);
    }
  };

  const inputClass = "ci-input";

  return (
    <div className="min-h-screen bg-[#FFFCF7]" style={{ backgroundImage: "radial-gradient(600px circle at 50% 0%, rgba(37,84,199,0.06), transparent 60%)" }}>
      <main className="flex min-h-screen items-center justify-center px-6 py-10">
        <div className="w-full max-w-[420px] rounded-xl border border-[#E5E5E5] bg-white p-8 shadow-[0_8px_24px_rgba(17,17,17,0.06),0_2px_6px_rgba(17,17,17,0.04)]">
          <div className="mb-8 text-center">
            <p className="text-[18px] font-semibold text-[#2554C7]">Credit<span className="text-[#111111]">IQ</span></p>
            <h1 className="mt-6 text-[24px] font-semibold text-[#111111]">Create account</h1>
            <p className="mt-2 text-[13px] text-[#737373]">Start a clean credit risk analysis workspace.</p>
          </div>

          <div className="space-y-5">
            <label className="block">
              <span className="mb-2 block text-[12px] font-medium text-[#404040]">Full name</span>
              <div className="ci-auth-field">
                <span className="ci-auth-icon"><User className="h-4 w-4" /></span>
                <input className={inputClass} value={name} onChange={(e) => { setName(e.target.value); setMessage(""); }} onKeyDown={(e) => e.key === "Enter" && register()} placeholder="Your name" />
              </div>
            </label>

            <label className="block">
              <span className="mb-2 block text-[12px] font-medium text-[#404040]">Email address</span>
              <div className="ci-auth-field">
                <span className="ci-auth-icon"><Mail className="h-4 w-4" /></span>
                <input className={inputClass} value={email} onChange={(e) => { setEmail(e.target.value); setMessage(""); }} onKeyDown={(e) => e.key === "Enter" && register()} placeholder="you@example.com" type="email" />
              </div>
            </label>

            <label className="block">
              <span className="mb-2 block text-[12px] font-medium text-[#404040]">Password</span>
              <div className="ci-auth-field">
                <span className="ci-auth-icon"><Lock className="h-4 w-4" /></span>
                <input className={`${inputClass} pr-10`} value={password} onChange={(e) => { setPassword(e.target.value); setMessage(""); }} onKeyDown={(e) => e.key === "Enter" && register()} placeholder="At least 6 characters" type={showPassword ? "text" : "password"} />
                <button type="button" onClick={() => setShowPassword((value) => !value)} className="absolute right-3 top-1/2 -translate-y-1/2 text-[#737373] hover:text-[#111111]">
                  {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
            </label>

            <button onClick={register} disabled={loading} className="ci-button h-10 w-full disabled:opacity-50">
              {loading ? "Creating account..." : <>Create account <ArrowRight className="h-[15px] w-[15px]" /></>}
            </button>

            {message && (
              <div className={`rounded-lg border p-3 text-[13px] font-medium ${messageTone === "success" ? "border-[#BFE2C2] bg-[#EEF6EE] text-[#15803D]" : "border-[#F3C6C3] bg-[#FBECEB] text-[#B91C1C]"}`}>
                {message}
              </div>
            )}

            <p className="text-center text-[13px] text-[#737373]">
              Already have an account? <Link to="/login" className="font-medium text-[#2554C7] hover:underline">Sign in</Link>
            </p>
            <p className="border-t border-[#E5E5E5] pt-4 text-center text-[12px] leading-5 text-[#737373]">
              Logistic Regression, Random Forest, SHAP explainability, and model analytics in one focused admin interface.
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}



