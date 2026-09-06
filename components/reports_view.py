import streamlit as st
import html
import textwrap

def render_reports_view(reports: list, title: str = "Verified Multimodal Intelligence Reports"):
    """
    Renders actual YouTube & verified social reports with thumbnail, title, channel,
    hazard category, verification status, confidence score, reason, and [ WATCH VIDEO ] link.
    Uses textwrap.dedent and unsafe_allow_html=True to prevent raw HTML display.
    """
    if not reports:
        st.info("ℹ️ No social or YouTube reports match the selected filters.")
        return

    header_html = f"""
<div style="display: flex; justify-content: space-between; align-items: center; margin: 16px 0 12px 0;">
    <div>
        <h3 style="margin: 0; font-size: 18px; font-weight: 700; color: #f8fafc;">
            📹 {title} ({len(reports)} records)
        </h3>
        <p style="margin: 2px 0 0 0; font-size: 12px; color: #94a3b8;">
            Multimodal cross-verification against physical ground-truth weather sensors
        </p>
    </div>
    <div style="background: rgba(234, 179, 8, 0.15); border: 1px solid rgba(234, 179, 8, 0.3); border-radius: 8px; padding: 4px 10px; font-size: 11px; color: #facc15; font-weight: 600;">
        🔒 SHA-256 Deduplication Active
    </div>
</div>
"""
    st.markdown(textwrap.dedent(header_html).strip(), unsafe_allow_html=True)

    # 2 reports per row in modern card layout
    for i in range(0, len(reports), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(reports):
                with cols[j]:
                    _render_single_report_card(reports[i + j])

def _render_single_report_card(report: dict):
    # Extract fields with safe fallbacks
    title_raw = report.get("content_text") or report.get("title") or "Weather Observation Report"
    title = html.escape(str(title_raw))
    
    source_url = report.get("source_url") or report.get("video_url") or "#"
    source_id = report.get("source_id") or report.get("video_id") or ""
    channel = report.get("channel") or report.get("source_type") or "YouTube Channel"
    
    # Thumbnail URL resolution
    thumbnail = report.get("media_url") or report.get("thumbnail_url")
    if not thumbnail and source_id:
        thumbnail = f"https://img.youtube.com/vi/{source_id}/hqdefault.jpg"
    elif not thumbnail:
        thumbnail = "https://images.unsplash.com/photo-1534088568595-a066f410bcda?w=600&auto=format&fit=crop&q=60"

    hazard_category = report.get("hazard_category") or report.get("event_category") or "Severe Weather"
    status = str(report.get("verification_status") or "UNVERIFIED").upper()
    confidence = float(report.get("verification_confidence") or 0.0)
    confidence_pct = confidence * 100 if confidence <= 1.0 else confidence
    reason = html.escape(str(report.get("verification_reason") or "Cross-sensor verification pending analysis."))
    location = report.get("extracted_location") or "Chennai"
    fingerprint = report.get("fingerprint") or "N/A"
    short_fp = f"{fingerprint[:12]}...{fingerprint[-8:]}" if len(fingerprint) > 20 else fingerprint

    # Status color coding
    if "SUPPORTED" in status and "PARTIALLY" not in status:
        status_bg = "rgba(16, 185, 129, 0.2)"
        status_border = "#10b981"
        status_color = "#34d399"
        status_icon = "✅"
    elif "PARTIALLY" in status:
        status_bg = "rgba(59, 130, 246, 0.2)"
        status_border = "#3b82f6"
        status_color = "#60a5fa"
        status_icon = "⚠️"
    elif "CONTRADICTED" in status:
        status_bg = "rgba(239, 68, 68, 0.2)"
        status_border = "#ef4444"
        status_color = "#f87171"
        status_icon = "❌"
    else:
        status_bg = "rgba(100, 116, 139, 0.2)"
        status_border = "#64748b"
        status_color = "#94a3b8"
        status_icon = "⏳"

    card_html = f"""
<div style="background: rgba(30, 41, 59, 0.85); border: 1px solid rgba(71, 85, 105, 0.4); border-radius: 14px; overflow: hidden; margin-bottom: 16px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 4px 16px rgba(0,0,0,0.2);">
    <div style="position: relative; height: 180px; width: 100%; overflow: hidden; background: #0f172a;">
        <img src="{thumbnail}" style="width: 100%; height: 100%; object-fit: cover; opacity: 0.9;" alt="Report Media"/>
        <div style="position: absolute; top: 10px; left: 10px; background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(255, 255, 255, 0.2); backdrop-filter: blur(4px); padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 700; color: #38bdf8;">
            📍 {location}
        </div>
        <div style="position: absolute; top: 10px; right: 10px; background: {status_bg}; border: 1px solid {status_border}; backdrop-filter: blur(4px); padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 800; color: {status_color};">
            {status_icon} {status}
        </div>
        <div style="position: absolute; bottom: 8px; left: 10px; background: rgba(0,0,0,0.75); padding: 2px 8px; border-radius: 4px; font-size: 10.5px; color: #e2e8f0;">
            🏷️ {hazard_category}
        </div>
    </div>

    <div style="padding: 14px 16px; flex-grow: 1; display: flex; flex-direction: column; justify-content: space-between;">
        <div>
            <h4 style="margin: 0 0 6px 0; font-size: 14px; font-weight: 600; color: #f8fafc; line-height: 1.4; height: 40px; overflow: hidden; text-overflow: ellipsis; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;">
                {title}
            </h4>
            
            <div style="display: flex; justify-content: space-between; font-size: 11px; color: #94a3b8; margin-bottom: 8px;">
                <span>📺 Channel: <strong style="color: #cbd5e1;">{channel}</strong></span>
                <span>Confidence: <strong style="color: {status_color};">{confidence_pct:.0f}%</strong></span>
            </div>

            <div style="background: rgba(15, 23, 42, 0.6); border-radius: 8px; padding: 8px 10px; margin-bottom: 10px; border-left: 3px solid {status_border};">
                <div style="font-size: 10px; text-transform: uppercase; color: #94a3b8; font-weight: 700; margin-bottom: 2px;">Verification Reason</div>
                <div style="font-size: 11px; color: #e2e8f0; line-height: 1.3;">
                    {reason}
                </div>
            </div>
        </div>

        <div>
            <div style="font-size: 9.5px; color: #64748b; font-family: monospace; margin-bottom: 10px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                SHA-256: {short_fp}
            </div>

            <a href="{source_url}" target="_blank" style="text-decoration: none; display: block;">
                <div style="background: linear-gradient(135deg, #ef4444, #dc2626); color: white; text-align: center; padding: 8px 12px; border-radius: 8px; font-size: 12px; font-weight: 700; display: flex; align-items: center; justify-content: center; gap: 6px; box-shadow: 0 2px 6px rgba(220, 38, 38, 0.4); transition: background 0.2s;">
                    <span>▶️</span> WATCH VIDEO
                </div>
            </a>
        </div>
    </div>
</div>
"""
    st.markdown(textwrap.dedent(card_html).strip(), unsafe_allow_html=True)
