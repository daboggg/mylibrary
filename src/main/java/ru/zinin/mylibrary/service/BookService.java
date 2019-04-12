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

    public void addBookFile(String bookname,
                            String author,
                            User user,
                            MultipartFile file,
                            MultipartFile picture,
                            Long bookId
    ) throws IOException {
        Book book;
        if (bookId!=null){
            book = bookRepo.findBookById(bookId);

            //свойства книги, (имя, фамилия, название, аннотация)
            String[] bookProp = fileService.bookProp(book.getFilename());

            book.setReliser(user);
            if (!StringUtils.isEmpty(bookname)) {
                book.setBookname(bookname);
            } else {
                if (bookProp[2] != null) {
                    book.setBookname(bookProp[2]);
                }
            }
            if (!StringUtils.isEmpty(author)) {
                book.setAuthor(author);
            } else {
                if (bookProp[0] != null && bookProp[1] != null) {
                    book.setAuthor(bookProp[0] + " " + bookProp[1]);
                }
            }
            //добавляем картинку
            addPictureFile(picture, book);

            // добавляем книгу
            addBookFile(bookname, author, file, book);

        }
        else {
            book = new Book();
            book.setBookname(bookname);
            book.setReliser(user);
            book.setAuthor(author);

            //добавляем картинку
            addPictureFile(picture, book);

            // добавляем книгу
            addBookFile(bookname, author, file, book);
        }

        bookRepo.save(book);
    }

    //добавляем книгу
    private void addBookFile(String bookname,
                             String author,
                             MultipartFile file,
                             Book book
    ) throws IOException {
        if (file != null && !file.isEmpty()) {
            String uuidFile = getString();
            String resultFilename = uuidFile + "." + file.getOriginalFilename();

            // загружаем файл на сервер
            file.transferTo(new File(uploadPath + "/" + resultFilename));
            book.setFilename(resultFilename);

            //свойства книги, (имя, фамилия, название, аннотация)
            String[] bookProp = fileService.bookProp(resultFilename);

            //если автор не определен, берем автора из книги
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
    }

    //добавляем картинку
    private void addPictureFile(MultipartFile picture, Book book) throws IOException {
        if (picture != null && !picture.isEmpty()) {
            String uuidFile = getString();
            String resultFilename = uuidFile + "." + picture.getOriginalFilename();
            // загружаем картинку на сервер
            picture.transferTo(new File(uploadPath + "/" + resultFilename));
            book.setPictureName(resultFilename);
        }
    }

    private String getString() {
        File uploadDir = new File(uploadPath);
        if (!uploadDir.exists()) {
            uploadDir.mkdir();
        }
        return UUID.randomUUID().toString();
    }

    // поиск по автору или по названию
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
