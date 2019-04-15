package ru.zinin.mylibrary.repos;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import ru.zinin.mylibrary.domain.Book;
import ru.zinin.mylibrary.domain.User;

import java.util.List;

public interface BookRepo extends JpaRepository<Book, Long> {
    Page<Book> findAll(Pageable pageable);
    Page<Book> findByAuthor(String author, Pageable pageable);
    Page<Book> findByBookname(String bookname, Pageable pageable);
    Page<Book> findByReliser(User user, Pageable pageable);

    Book findBookById(Long id);
}
