package ru.zinin.mylibrary.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import ru.zinin.mylibrary.domain.Book;
import ru.zinin.mylibrary.domain.Role;
import ru.zinin.mylibrary.domain.User;
import ru.zinin.mylibrary.repos.BookRepo;
import ru.zinin.mylibrary.service.BookService;

import java.util.List;

@Controller
public class MainController {

    @Autowired
    private BookRepo bookRepo;

    @Autowired
    private BookService bookService;

    @GetMapping("/")
    public String homePage() {
        return "home_page";
    }

    @GetMapping("/main")
    public String main(
            @RequestParam(required = false)String filter,
            @RequestParam(required = false) String type,
            Model model
    ) {
        List<Book> books = bookService.searchBook(filter, type);
        model.addAttribute("filter", filter);
        model.addAttribute("type", type);
        model.addAttribute("books", books);
        return "main";
    }

    @PostMapping("/add")
    public String addBook(
            @AuthenticationPrincipal User user,
            @RequestParam String bookname,
            @RequestParam String author,
            Model model
    ) {
        bookService.addBook(bookname, author,user);
        model.addAttribute("books", bookRepo.findAll());
        return "main";
    }

}
