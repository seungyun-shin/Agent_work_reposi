// 판매 설정 — 사용자가 결제 링크를 만들면 checkoutUrl만 채우면 사이트 전체에 반영된다.
window.SITE = {
  checkoutUrl: "",          // 예: "https://xxxx.gumroad.com/l/ai-kit"
  price: "12,900원",
  listPrice: "19,900원",
  product: "퇴근을 앞당기는 AI 업무자동화 키트",
};
document.addEventListener("DOMContentLoaded", () => {
  const s = window.SITE;
  document.querySelectorAll("[data-buy]").forEach((a) => {
    if (s.checkoutUrl) {
      a.href = s.checkoutUrl;
    } else {
      a.href = (document.querySelector("meta[name=root]")?.content || "") + "free-prompts.html";
      a.textContent = "오픈 준비 중 · 무료 샘플 먼저 보기";
    }
  });
  document.querySelectorAll("[data-price]").forEach((e) => (e.textContent = s.price));
  document.querySelectorAll("[data-list-price]").forEach((e) => (e.textContent = s.listPrice));
});
