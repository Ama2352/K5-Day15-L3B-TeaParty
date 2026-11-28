# Khảo sát: chuẩn bị phản ánh vấn đề ở nơi làm việc

- Công cụ: Google Form, ẩn danh, không thu email.
- Kênh đã gửi: Zalo
- Giờ mở: 19:09 ngày 27/11/2026 · Giờ chốt: 19:27 ngày 27/11/2026
- Bản số liệu hiện tại: `results.csv`, lấy 27/11/2026; phản hồi từ 19:09:10 đến 19:27:21 (n = 21). Đã bỏ cột thời gian, thay bằng mã S01–S21.

## Nguyên bộ câu hỏi và phương án (mã tạo form)

```javascript
function taoForm(){
 var f=FormApp.create("Khảo sát: chuẩn bị phản ánh vấn đề ở nơi làm việc");
 f.setDescription("Chào bạn, nhóm sinh viên đang tìm hiểu cách người lao động chuẩn bị phản ánh các vấn đề ở nơi làm việc, như lương thưởng, an toàn lao động, phân biệt đối xử, hành vi thiếu tôn trọng hoặc quấy rối, để thiết kế một công cụ giúp việc này dễ hơn. Khảo sát ẩn danh, khoảng 9 phút. Bạn không cần kể chi tiết sự việc, có thể bỏ qua bất kỳ câu nào và dừng lúc nào cũng được. Khảo sát dành cho người từ 18 tuổi trở lên.");f.setCollectEmail(false);f.setLimitOneResponsePerUser(false);f.setProgressBar(true);
 f.setConfirmationMessage("Cảm ơn bạn đã tham gia. Nếu bạn hoặc người bạn biết cần hỗ trợ về bạo lực, quấy rối, bạn có thể liên hệ công đoàn cơ sở nơi làm việc hoặc Đường dây nóng hỗ trợ người bị bạo lực giới của CSAGA: 024 3333 5599 (miễn phí, bảo mật).");
 var q0=f.addMultipleChoiceItem().setTitle("Câu 0. Bạn từ 18 tuổi trở lên và đồng ý tham gia?").setRequired(true);
 var pA=f.addPageBreakItem().setTitle("Phần A. Bạn là ai").setHelpText("");
 var q1=f.addMultipleChoiceItem().setTitle("Câu 1. Vai trò chính của bạn trong công việc hiện tại").setRequired(false);
 q1.setChoiceValues(["Nhân viên, người lao động", "Quản lý trực tiếp", "Nhân sự hoặc người được giao tiếp nhận phản ánh", "Cán bộ công đoàn", "Luật sư, tư vấn viên hoặc người của tổ chức hỗ trợ", "Khác"]);
 var q2=f.addMultipleChoiceItem().setTitle("Câu 2. Độ tuổi").setRequired(false);
 q2.setChoiceValues(["18–24", "25–34", "35–44", "45 trở lên", "Không muốn trả lời"]);
 var q3=f.addMultipleChoiceItem().setTitle("Câu 3. Ngành nghề").setRequired(false);
 q3.setChoiceValues(["Văn phòng", "Nhà máy, xưởng", "Dịch vụ, bán lẻ, nhà hàng", "Giáo dục", "Y tế", "Làm tự do", "Khác"]);
 var q4=f.addMultipleChoiceItem().setTitle("Câu 4. Nơi làm việc có khoảng bao nhiêu người?").setRequired(false);
 q4.setChoiceValues(["Dưới 10", "10–50", "51–200", "Trên 200", "Không rõ"]);
 var q5=f.addMultipleChoiceItem().setTitle("Câu 5. Nơi làm việc có quy trình hoặc đầu mối nhận phản ánh không?").setRequired(false);
 q5.setChoiceValues(["Có, tôi biết rõ gửi cho ai", "Có nhưng tôi không rõ cách làm", "Không có", "Không biết"]);
 var pB=f.addPageBreakItem().setTitle("Phần B. Bao nhiêu người gặp, bao nhiêu lần").setHelpText("");
 var q6=f.addMultipleChoiceItem().setTitle("Câu 6. Trong 12 tháng qua, bạn hoặc người bạn biết có cần chuẩn bị một bản phản ánh kèm tài liệu (tin nhắn, ảnh, ghi chú, ghi âm) về vấn đề ở nơi làm việc không?").setRequired(false);
 var pB2=f.addPageBreakItem().setTitle("Phần B (tiếp)").setHelpText("");
 var q7=f.addCheckboxItem().setTitle("Câu 7. Vấn đề đó thuộc loại nào?").setChoiceValues(["Lương, thưởng, giờ làm", "An toàn lao động", "Phân biệt đối xử", "Lời nói hoặc hành vi thiếu tôn trọng", "Hành vi, tin nhắn hoặc đụng chạm mang tính tình dục khiến người khác khó chịu", "Khác"]);
 var q8=f.addMultipleChoiceItem().setTitle("Câu 8. Trong 12 tháng qua, khoảng bao nhiêu lần bạn (hoặc người đó) phải chuẩn bị hoặc bổ sung tài liệu như vậy?").setRequired(false);
 q8.setChoiceValues(["1 lần", "2–3 lần", "4–6 lần", "7–12 lần", "Trên 12 lần", "Không nhớ"]);
 var pC=f.addPageBreakItem().setTitle("Phần C. Lần gần nhất đã làm thế nào").setHelpText("Các câu dưới đây hỏi về lần gần nhất bạn hoặc người bạn biết chuẩn bị bản phản ánh như vậy.");
 var q9=f.addCheckboxItem().setTitle("Câu 9. Những việc nào đã được làm?").setChoiceValues(["Ghi lại sự việc bằng lời kể hoặc ghi chú", "Gom tin nhắn, hình ảnh, tài liệu liên quan", "Đối chiếu thông tin, sắp xếp mốc thời gian, tìm phần còn thiếu", "Viết bản phản ánh", "Tìm người hoặc tổ chức tiếp nhận, hỗ trợ", "Nhờ người khác viết hộ", "Không làm việc nào ở trên"]);
 var q10=f.addMultipleChoiceItem().setTitle("Câu 10. Việc nào mất nhiều thời gian hoặc công sức nhất?").setRequired(false);
 q10.setChoiceValues(["Ghi lại sự việc", "Gom tài liệu", "Đối chiếu, sắp xếp mốc, tìm phần thiếu", "Viết bản phản ánh", "Tìm nơi tiếp nhận", "Không nhớ"]);
 var q11=f.addMultipleChoiceItem().setTitle("Câu 11. Tổng thời gian để có bản phản ánh đủ dùng là bao lâu?").setRequired(false);
 q11.setChoiceValues(["Dưới 30 phút", "30 phút – 1 giờ", "1–3 giờ", "3–8 giờ", "Rải rác nhiều ngày", "Chưa xong", "Không nhớ"]);
 var q12=f.addMultipleChoiceItem().setTitle("Câu 12. Bản phản ánh đã được sửa hoặc viết lại mấy lần trước khi gửi?").setRequired(false);
 q12.setChoiceValues(["Không sửa", "1–2 lần", "3–5 lần", "Trên 5 lần", "Chưa gửi", "Không nhớ"]);
 var q13=f.addCheckboxItem().setTitle("Câu 13. Đã dùng những công cụ nào?").setChoiceValues(["Ghi chú trên điện thoại", "Word hoặc Google Docs", "Excel hoặc Google Sheets", "Chụp màn hình, thư mục ảnh", "ChatGPT, Gemini, Claude hoặc công cụ AI khác", "Mẫu tìm trên mạng", "Nhờ người khác", "Không dùng công cụ nào"]);
 var q14=f.addCheckboxItem().setTitle("Câu 14. Nếu có dùng AI, AI được dùng cho việc gì?").setChoiceValues(["Tóm tắt lời kể", "Viết lại cho mạch lạc", "Sắp xếp mốc thời gian", "Kiểm tra còn thiếu thông tin gì", "Đọc chữ trong ảnh", "Hỏi về quy định, quyền lợi", "Không dùng AI"]);
 f.addGridItem().setTitle("Câu 15. Mức độ khó của từng việc").setRows(["Gom tài liệu đang nằm rải rác", "Sắp xếp các mốc thời gian", "Biết mình còn thiếu thông tin gì", "Viết lại diễn biến cho rõ ràng", "Tìm người hoặc tổ chức tiếp nhận"]).setColumns(["1 rất dễ", "2", "3", "4", "5 rất khó", "Không làm"]);
 var q16=f.addMultipleChoiceItem().setTitle("Câu 16. Bản phản ánh đó cuối cùng ra sao?").setRequired(false);
 q16.setChoiceValues(["Đã gửi và được xử lý", "Đã gửi nhưng không có kết quả rõ ràng", "Định gửi nhưng thôi", "Không gửi", "Không biết"]);
 var pD=f.addPageBreakItem().setTitle("Phần D. Tình huống giả định").setHelpText("Phần này dành cho mọi người, kể cả người chưa từng chuẩn bị phản ánh. Minh làm nhân viên văn phòng. Trong khoảng hai tháng, một quản lý nhiều lần nhắn tin và nói những câu khiến Minh khó chịu, có lúc ngoài giờ làm. Minh có vài ảnh chụp màn hình tin nhắn, nhớ một số lần nói chuyện trực tiếp nhưng không nhớ chính xác ngày, và đang cân nhắc gửi phản ánh cho bộ phận nhân sự.");
 f.addGridItem().setTitle("Câu 17. Theo bạn, việc nào khó với Minh? Xếp hạng từ 1 (khó nhất) đến 5").setRows(["Ghi lại sự việc", "Gom ảnh, tin nhắn", "Đối chiếu, sắp xếp mốc, tìm phần thiếu", "Viết bản phản ánh", "Tìm nơi tiếp nhận"]).setColumns(["1","2","3","4","5"]).setValidation(FormApp.createGridValidation().requireLimitOneResponsePerColumn().build());
 var q18=f.addMultipleChoiceItem().setTitle("Câu 18. Bạn nghĩ Minh sẽ mất bao lâu để có bản phản ánh đủ dùng?").setRequired(false);
 q18.setChoiceValues(["Dưới 30 phút", "30 phút – 1 giờ", "1–3 giờ", "3–8 giờ", "Rải rác nhiều ngày", "Không bao giờ xong"]);
 var pE=f.addPageBreakItem().setTitle("Phần E. Ba hướng hỗ trợ").setHelpText("");
 f.addGridItem().setTitle("Câu 19. Mỗi kiểu hỗ trợ dưới đây hữu ích với Minh đến mức nào?").setRows(["Gom lời kể, ảnh, tài liệu và sắp xếp thành dòng thời gian", "Chỉ ra thông tin còn thiếu và gợi ý cách bổ sung", "Chuyển hồ sơ đã chuẩn bị tới luật sư hoặc tổ chức hỗ trợ khi Minh đồng ý"]).setColumns(["1 không hữu ích", "2", "3", "4", "5 rất hữu ích"]);
 var q20=f.addMultipleChoiceItem().setTitle("Câu 20. Nếu chỉ có một kiểu hỗ trợ, bạn chọn kiểu nào?").setRequired(false);
 q20.setChoiceValues(["Gom và sắp xếp", "Chỉ ra phần còn thiếu", "Kết nối luật sư, tổ chức hỗ trợ", "Không cần kiểu nào"]);
 var q21=f.addCheckboxItem().setTitle("Câu 21. Điều gì khiến bạn lo ngại khi dùng công cụ như vậy?").setChoiceValues(["Dữ liệu bị lộ hoặc bị công ty biết", "AI viết sai ý hoặc thêm chi tiết", "Không tin AI hiểu tiếng Việt", "Mất thời gian học cách dùng", "Sợ bản do AI viết bị coi nhẹ", "Không lo ngại gì", "Khác"]);
 q21.setValidation(FormApp.createCheckboxValidation().requireSelectAtMost(3).build());
 var qR=f.addMultipleChoiceItem().setTitle("Công việc của bạn có bao gồm việc tiếp nhận hoặc tư vấn phản ánh (nhân sự, công đoàn, luật sư, tư vấn viên) không?");
 var pF=f.addPageBreakItem().setTitle("Phần F. Dành cho người tiếp nhận").setHelpText("");
 var q22=f.addMultipleChoiceItem().setTitle("Câu 22. Trong 12 tháng qua, nơi bạn làm việc nhận khoảng bao nhiêu phản ánh liên quan đến hành vi thiếu tôn trọng hoặc quấy rối?").setRequired(false);
 q22.setChoiceValues(["0", "1–2", "3–5", "6–12", "Trên 12", "Không được phép chia sẻ"]);
 var q23=f.addCheckboxItem().setTitle("Câu 23. Phần lớn các bản phản ánh đó thường thiếu thông tin nào?").setChoiceValues(["Thời gian", "Địa điểm, bối cảnh", "Người liên quan, người chứng kiến", "Mô tả hành vi cụ thể", "Tài liệu kèm theo", "Đề nghị xử lý", "Thường không thiếu"]);
 var q24=f.addMultipleChoiceItem().setTitle("Câu 24. Trung bình mất bao lâu để làm rõ thông tin của một bản phản ánh trước khi xử lý?").setRequired(false);
 q24.setChoiceValues(["Dưới 1 giờ", "1–3 giờ", "3–8 giờ", "Nhiều ngày", "Không rõ"]);
 var pEnd=f.addPageBreakItem().setTitle("Kết thúc").setHelpText("");
 f.addParagraphTextItem().setTitle('Góp ý thêm (không bắt buộc)').setHelpText("Vui lòng không ghi tên người hoặc tên công ty.");
 f.addMultipleChoiceItem().setTitle("Bạn có muốn tham gia buổi thử công cụ 30 phút với tình huống giả định không?").setHelpText("Nếu có, nhóm sẽ gửi đường link form liên hệ riêng sau khi bạn gửi khảo sát.").setChoiceValues(['Có','Không']);
 q0.setChoices([q0.createChoice("Có, tôi đồng ý",pA),q0.createChoice("Không (form kết thúc)",FormApp.PageNavigationType.SUBMIT)]);
 q6.setChoices([q6.createChoice("Có, chính tôi",pB2),q6.createChoice("Có, người tôi biết",pB2),q6.createChoice("Cả hai",pB2),q6.createChoice("Không",pD),q6.createChoice("Không nhớ",pD)]);
 qR.setChoices([qR.createChoice('Có',pF),qR.createChoice('Không',pEnd)]);
 Logger.log('Sửa form: '+f.getEditUrl());Logger.log('Link gửi: '+f.getPublishedUrl());
}
```
