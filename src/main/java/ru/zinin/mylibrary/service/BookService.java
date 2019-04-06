package ru.zinin.mylibrary.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;
import ru.zinin.mylibrary.domain.Book;
import ru.zinin.mylibrary.domain.User;
import ru.zinin.mylibrary.repos.BookRepo;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

@Service
public class BookService {

    @Autowired
    private BookRepo bookRepo;

    public void addBook(String bookname, String author, User user) {

        bookRepo.save(new Book(bookname, author, user));

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
