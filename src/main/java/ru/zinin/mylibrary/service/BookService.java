package ru.zinin.mylibrary.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;
import org.springframework.web.multipart.MultipartFile;
import ru.zinin.mylibrary.domain.Book;
import ru.zinin.mylibrary.domain.User;
import ru.zinin.mylibrary.repos.BookRepo;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.UUID;

@Service
public class BookService {

    @Autowired
    private BookRepo bookRepo;

    @Value("${upload.path}")
    private String uploadPath;

    @Autowired
    private FileService fileService;

    public void addBook(String bookname,
                        String author,
                        User user,
                        MultipartFile file
    ) throws IOException {
        Book book = new Book();
        book.setBookname(bookname);
        book.setReliser(user);
        book.setAuthor(author);

        if (file != null&&!file.isEmpty()) {
            File uploadDir = new File(uploadPath);
            if (!uploadDir.exists()) {
                uploadDir.mkdir();
            }
            String uuidFile = UUID.randomUUID().toString();
            String resultFilename = uuidFile + "." + file.getOriginalFilename();

            // загружаем файл на сервер
            file.transferTo(new File(uploadPath + "/" + resultFilename));
            book.setFilename(resultFilename);

            //свойства книги, (имя, фамилия, название, аннотация)
            String[] bookProp = fileService.bookProp(resultFilename);

            //если автор не определен, берем название из книги
            if (author == null || StringUtils.isEmpty(author)) {
                if (bookProp[0] != null && bookProp[1] != null) {
                    book.setAuthor(bookProp[0] + " " + bookProp[1]);
                }
            }
            //если название книги не определено, берем название из книги
            if (bookname == null || StringUtils.isEmpty(bookname)) {
                if (bookProp[2] != null) {
                    book.setBookname(bookProp[2]);
                }
            }
        }

        bookRepo.save(book);
    }

    public List<Book> searchBook(String filter, String type) {
        List<Book> result = new ArrayList<>();

        if (type != null && type.equals("name") && filter != null && !StringUtils.isEmpty(filter)) {
            result = bookRepo.findByBookname(filter);
        }
        if (type != null && type.equals("author") && filter != null && !StringUtils.isEmpty(filter)) {
            result = bookRepo.findByAuthor(filter);
        }
        return result.size() == 0 ? bookRepo.findAll() : result;
    }
}
