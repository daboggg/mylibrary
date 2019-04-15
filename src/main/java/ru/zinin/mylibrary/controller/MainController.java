package ru.zinin.mylibrary.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.data.web.PageableDefault;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;
import ru.zinin.mylibrary.domain.Book;
import ru.zinin.mylibrary.domain.User;
import ru.zinin.mylibrary.repos.BookRepo;
import ru.zinin.mylibrary.service.BookService;
import ru.zinin.mylibrary.service.FileService;

import java.io.IOException;
import java.util.*;
import java.util.stream.Collectors;

@Controller
public class MainController {

    @Autowired
    private BookRepo bookRepo;

    @Autowired
    private BookService bookService;

    @Autowired
    private FileService fileService;

    @GetMapping("/")
    public String homePage() {
        return "home_page";
    }

    @GetMapping("/main")
    public String main(
            @RequestParam(required = false)String filter,
            @RequestParam(required = false) String type,
            Model model,
            @PageableDefault(sort = {"id"},direction = Sort.Direction.DESC)Pageable pageable
            ) {
        Page<Book> page = bookService.searchBook(filter, type, pageable);
        // добавляем аннотации к каждой книге
        addAnnotation(page);
        model.addAttribute("filter", filter);
        model.addAttribute("type", type);
        model.addAttribute("url", "/main");
        model.addAttribute("page", page);
        return "main";
    }

    @PostMapping("/main")
    public String addBook(
            @AuthenticationPrincipal User user,
            @RequestParam String bookname,
            @RequestParam String author,
            @RequestParam("file") MultipartFile file,
            @RequestParam("picture")MultipartFile picture,
            Model model,
            @PageableDefault(sort = {"id"},direction = Sort.Direction.DESC)Pageable pageable
    ) throws IOException {
        bookService.addBookFile(bookname, author,user,file,picture,null);

        Page<Book> allBooks = bookRepo.findAll(pageable);
        // добавляем аннотации к каждой книге
        addAnnotation(allBooks);
        model.addAttribute("books", allBooks);
        return "redirect:/main";
    }

    private void addAnnotation(Page<Book> allBooks) {
        allBooks.forEach(item -> item.setAnnotation(fileService.bookProp(item.getFilename())[3] == null ? "No annotation" : fileService.bookProp(item.getFilename())[3]));
    }

    private void addAnnotation(Collection<Book> allBooks) {
        allBooks.forEach(item -> item.setAnnotation(fileService.bookProp(item.getFilename())[3] == null ? "No annotation" : fileService.bookProp(item.getFilename())[3]));
    }

    @GetMapping("/user-books/{user}")
    public String userBooks(
            @AuthenticationPrincipal User currentUser,
            @PathVariable User user,
            Model model,
            @RequestParam(required = false) Book book,
            @PageableDefault(sort = {"id"},direction = Sort.Direction.DESC)Pageable pageable
    ) {
//        List<Book> books = user.getBooks().stream().collect(Collectors.toList());
        Page<Book> page = bookRepo.findByReliser(user,pageable);
//        System.out.println(page.getTotalElements());
        // добавляем аннотации к каждой книге
        addAnnotation(page.getContent());
//        model.addAttribute("books", books);
        model.addAttribute("book", book);
        model.addAttribute("url", "/user-books/"+user.getId());
        model.addAttribute("page", page);
        model.addAttribute("isCurrentUser", currentUser.equals(user));
        return "my_books";
    }

    @PostMapping("/user-books/{user}")
    public String updateBook(
            @AuthenticationPrincipal User currentUser,
            @PathVariable Long user,
            @RequestParam("id") Book book,
            @RequestParam String bookname,
            @RequestParam String author,
            @RequestParam("file") MultipartFile file,
            @RequestParam("picture")MultipartFile picture
    ) throws IOException {
        if (book!=null&&book.getReliser().equals(currentUser)) {
            bookService.addBookFile(bookname, author,currentUser,file,picture,book.getId());
        }
        return "redirect:/user-books/" + user;
    }
}
